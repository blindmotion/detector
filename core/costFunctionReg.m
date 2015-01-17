 function [J, grad] = costFunctionReg(theta, X, y, lambda)
    m = length(y); 

    J = sumsq(X*theta -y) / (2 * m) + sumsq(theta) * lambda;
    grad = (1 / m) .* ((X*theta-y)' * X);
end