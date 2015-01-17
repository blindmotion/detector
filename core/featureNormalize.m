function [X_norm, mu, sigma] = featureNormalize(X)
    X_norm = X;
    mu = zeros(1, size(X, 2));
    sigma = zeros(1, size(X, 2));

    mu = mean(X);
    sigma = std(X);
    
    sigma(sigma == 0) = 0.0001;
    
    X_norm = (X - mu) ./ sigma;
end 
