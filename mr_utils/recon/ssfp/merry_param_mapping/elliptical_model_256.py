
def EllipticalModel256(I1, I2, I3, I4):
    '''This function will attempt to follow the ellpitical signal model in the
    paper by Xiang, Qing-San and Hoff, Michael N. "Banding Artifact Removal
    for bSSFP Imaging with an Elliptical Signal Model", 2014.
    The function returns a complex image.

    I1 and I3 form one pair of 180 degree offset images, and I2 and I4 form
    the other pair.
    '''

    # Iterate through each pixel and calculate M directly; then compare it to
    # the maximum magnitude of all four input images.  If it is greater,
    # replace it with the complex sum value.
    M = np.zeros(256, 256)
    maximum = np.max(np.abs(I1), np.abs(I2))
    maximum = np.max(np.abs(I3), np.maximum)
    maximum = np.max(np.abs(I4), np.maximum)
    CS = (I1 + I2 + I3 + I4)/4
    for k in range(256):
        for n in range(256):
            M[k, n] = ((np.real(I1[k, n])*np.imag(I3[k, n]) - np.real(I3[k, n])*np.imag(I1[k, n]))*(I2[k, n] - I4[k, n]) - (np.real(I2[k, n])*np.imag(I4[k, n]) - np.real(I4[k, n])*np.imag(I2[k, n]))*(I1[k, n] - I3[k, n]))/((np.real(I1[k, n]) - np.real(I3[k, n]))*(np.imag(I2[k, n]) - np.imag(I4[k, n])) + (np.real(I2[k, n]) - np.real(I4[k, n]))*(np.imag(I3[k, n]) - np.imag(I1[k, n]))) # Equation (13)
            if (np.abs(M[k, n]) > np.maximum(k, n)) or np.isnan(M[k, n]):
                # This removes the really big singularities; without this the
                # image is mostly black.
                M[k, n] = CS[k, n]

    # Calculate the weight w for each pixel.
    w1 = np.zeros(256, 256) # bottle is 512 x 256
    w2 = np.zeros(256, 256)
    for k in range(256): # bottle is 512
        for n in range(256):
            numerator1 = 0
            denominator1 = 0
            numerator2 = 0
            denominator2 = 0
            for x = -2:2
                a = k + x;
                for y = -2:2
                    b = n + y;
                    if (a < 1) || (b < 1) || (a > 256) || (b > 256)

                    else
                        numerator1 = numerator1 + conj(I3(a,b) - M(a,b)) * (I3(a,b) - I1(a,b)) + ...
                            conj(I3(a,b) - I1(a,b)) * (I3(a,b) - M(a,b));
                        denominator1 = denominator1 + conj(I1(a,b) - I3(a,b)) * (I1(a,b) - I3(a,b));
                        numerator2 = numerator2 + conj(I4(a,b) - M(a,b)) * (I4(a,b) - I2(a,b)) + ...
                            conj(I4(a,b) - I2(a,b)) * (I4(a,b) - M(a,b));
                        denominator2 = denominator2 + conj(I2(a,b) - I4(a,b)) * (I2(a,b) - I4(a,b));
                    end
                end
            end
            w1(k,n) = numerator1 / (2 * denominator1); % Equation (18) - first pair
            w2(k,n) = numerator2 / (2 * denominator2); % Equation (18) - second pair
        end
    end

    % Calculate the average weighted sum of image pairs.
    I = (I1 .* w1 + I3 .* (1 - w1) + I2 .* w2 + I4 .* (1 - w2)) / 2; % Equation (14) - averaged

    return I
