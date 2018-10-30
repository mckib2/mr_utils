from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import numpy as np
from mr_utils.load_data import load_mat
import matplotlib.pyplot as plt
import warnings # We know skimage will complain about importing imp...
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from skimage.util.shape import view_as_windows

# Distance callback
def create_distance_callback(dist_matrix):
  # Create a callback to calculate distances between cities.

  def distance_callback(from_node,to_node):
    return int(dist_matrix[from_node][to_node])

  return distance_callback

def get_slice(lpf=True,lpf_factor=6):
    # load data
    filename = '/home/nicholas/Documents/research/reordering_data/nufft_recons/ReconData/Trio/P010710/meas_MID42_CV_Radial7Off_triple_2.9ml_FID242_Kspace.npy'
    data = np.load(filename)

    # data shape is (x,y,frames,slices), choose a slice
    im = data[:,:,:,0]

    #  Take only the middle square of kspace, size determined by lpf_factor
    if lpf:
        center_pad = im.shape[0]/lpf_factor
        kspace = np.fft.fftshift(np.fft.fft2(im,axes=(0,1)))
        kspace[:int(kspace.shape[0]/2-center_pad),:,:] = 0
        kspace[int(kspace.shape[0]/2+center_pad):,:,:] = 0
        kspace[:,:int(kspace.shape[1]/2-center_pad),:] = 0
        kspace[:,int(kspace.shape[1]/2+center_pad):,:] = 0
        im = np.fft.ifft2(kspace,axes=(0,1))

    return(im)

def get_time_series(im,x=100,y=100,real_part=True,patch=False,patch_pad=(1,1)):

    # Do real/imag independently
    if real_part:
        im = im.real
    else:
        im = im.imag

    # Separate into time series at each (x,y)
    if not patch:
        time_series0 = im[x,y,:]
    else:
        # Pad to make sure we don't run off the edge when forming patches
        im = np.pad(im,((1,1),(1,1),(0,0)),mode='edge')

        # Adjust x,y because we padded!
        x += patch_pad[0]
        y += patch_pad[1]

        # Find the time series patch, take mean of patch and use that as value
        time_series0 = np.mean(im[x-patch_pad[0]:x+patch_pad[0]+1,y-patch_pad[1]:y+patch_pad[1]+1,:],axis=(0,1))

    return(time_series0)

def normalize_time_series(time_series0):
    # Normalize the series (scale up, scale up even more, make nonnegative, make integers)
    time_series = time_series0/np.max(time_series0)
    time_series *= 1e8
    time_series += np.abs(np.min(time_series))
    time_series = time_series.astype(int)

    # Make sure we're resolving float to int conversion
    # plt.plot(time_series)
    # plt.show()

    return(time_series)

def get_dist_matrix():

    time_series0 = get_time_series()
    time_series = normalize_time_series(time_series0)

    # Create distance matrix for the time series
    dist_matrix = np.tile(time_series,(time_series.size,1))
    dist_matrix -= dist_matrix.T
    dist_matrix = np.abs(dist_matrix)
    # print(dist_matrix)

    # # Double check that we're doing the right thing
    # N = time_series.size
    # dist_matrix = np.zeros((N,N))
    # for ii in range(N):
    #     for jj in range(N):
    #         # dist_matrix[ii,jj] = np.abs(time_series[ii] - time_series[jj])
    #         dist_matrix[ii,jj] = np.sqrt((time_series[ii].real - time_series[jj].real)**2 + (time_series[ii].imag - time_series[jj].imag)**2)
    # # assert(np.allclose(dist_matrix,dist_matrix0))

    # print(dist_matrix)
    return(dist_matrix,time_series0)

def ortools_tsp_solver():
    # Distance matrix and time series
    dist_matrix,time_series = get_dist_matrix()

    tsp_size = np.diag(dist_matrix).size
    node_names = list(range(tsp_size))

    num_routes = 1
    depot = int(np.argmin(time_series)) # start/stop index
    print('depot: %d' % depot)

    # Create routing model
    if tsp_size > 0:
        routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        # search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        # search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING)
        # search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH)
        # search_parameters.time_limit_ms = 60000

        # Create the distance callback.
        dist_callback = create_distance_callback(dist_matrix)
        routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
        # Solve the problem.
        assignment = routing.SolveWithParameters(search_parameters)
        if assignment:
            # Solution distance.
            print('Total distance: %s miles' % str(assignment.ObjectiveValue()))
            # Display the solution.
            # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
            route_number = 0
            index = routing.Start(route_number) # Index of the variable for the starting node.
            route = ''
            reorder = list()
            while not routing.IsEnd(index):
                # Convert variable indices to node indices in the displayed route.
                route += str(node_names[routing.IndexToNode(index)]) + ' -> '
                reorder.append(index)
                index = assignment.Value(routing.NextVar(index))
            route += str(node_names[routing.IndexToNode(index)])
            reorder = np.array(reorder).astype(int)


            # Results
            print('Route:')
            print(route)
            print('Reorder:')
            print(reorder)

            plt.plot(time_series[reorder])
            plt.plot(sorted(time_series))
            plt.show()

        else:
            print('No solution found.')
    else:
        print('Specify an instance greater than 0.')

    return(time_series,reorder)


def generate_orderings(im=None):
    patch = True
    patch_size = (3,3)
    lpf = True
    lpf_factor = 6

    if im is None:
        im = get_slice(lpf=lpf,lpf_factor=lpf_factor)

    # Split into real,imag
    im_real = im.real
    im_imag = im.imag

    if patch:
        for kk in range(im.shape[-1]):
            patches = view_as_windows(np.ascontiguousarray(im[:,:,kk]),patch_size)
            im_real[1:-1,1:-1,kk] = np.mean(patches.real,axis=(-1,-2))
            im_imag[1:-1,1:-1,kk] = np.mean(patches.imag,axis=(-1,-2))

    idx_real = np.argsort(im_real,axis=-1)
    idx_imag = np.argsort(im_imag,axis=-1)

    return(idx_real,idx_imag)


if __name__ == '__main__':
    # time_series,reorder = ortools_tsp_solver()
    #
    # # compute gradient of time_series proper
    # time_series_grad = np.gradient(time_series)
    #
    # # compute gradient of time_series reordered
    # time_series_reordered_grad = np.gradient(time_series[reorder])
    #
    # # compute gradient of time_series naive reordering
    # time_series_naive_reordered_grad = np.gradient(sorted(time_series))
    #
    # plt.plot(time_series_grad,label='Time Series')
    # plt.plot(time_series_reordered_grad,label='TSP Reordered')
    # plt.plot(time_series_naive_reordered_grad,label='Naive Reordered')
    # plt.legend()
    # plt.show()

    # Recognize that this problem is made up of cities at elevation pixel value.
    # Therefore the most efficient path is to traverse them in elevation order.
    # This is simply sorting the pixel values...

    generate_orderings()
