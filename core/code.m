1;

function [theta, J] = train(Train, TrainY, lambda, maxIter)
    fprintf('Training on %d values\n', size(Train, 1));

    initial_theta = zeros(size(Train, 2), 1);

    [cost, grad] = costFunctionReg(initial_theta, Train, TrainY, lambda);

    fprintf('Cost at initial theta (zeros): %f\n', cost);

    options = optimset('GradObj', 'on', 'MaxIter', maxIter);

    [theta, J, exit_flag] = ...
        fminunc(@(t)(costFunctionReg(t, Train, TrainY, lambda)), initial_theta, options);

    fprintf('Cost after optimization: %f\n', J);

    [cost, grad] = costFunctionReg(theta, Train, TrainY, 0);

    fprintf('Cost without regularization: %f\n', cost);
end

function p = predict(theta, X)
    p = round(X * theta);
    %p(p < 0) = 0;
end
