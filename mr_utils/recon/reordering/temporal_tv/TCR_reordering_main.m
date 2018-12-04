% Program to reconstruct undersampled DCE MRI data using temporal Total
% Variation constraint with reordering

% Ref: G. Adluru, E.V.R. DiBella. Reordering for improved constrained reconstruction from undersampled k-space data.
% International Journal of Biomedical Imaging vol. 2008, Article ID 341684, 12 pages, 2008. doi:10.1155/2008/341684.


clear all;

weight_fidelity = 1;
weight_temporal = 0.01;
beta_sqrd = 0.0000001;
noi = 200;

load Coil6.mat
load mask_k_space_sparse.mat

reduced_k_space = Coil.*mask_k_space_sparse;
prior = generate_prior(reduced_k_space);
recon_data = recon_tcr_reorder(prior,reduced_k_space,mask_k_space_sparse,noi,weight_fidelity,weight_temporal,beta_sqrd);

load reduced_data.mat

% for i = 1:70
%     subplot(1,2,1),imagesc(fliplr(abs(reduced_data(:,:,i)))),colormap gray,brighten(0.5),title('Reduced data')
%     subplot(1,2,2),imagesc(fliplr(abs(recon_data(:,:,i)))),colormap gray,brighten(0.5),title('Reconstructed data with reordering')
%     pause
% end
