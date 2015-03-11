source code.m

format none
warning("off")

arg_list = argv();
fileDat = arg_list{1};
outFile = arg_list{2};

configFile = "";

lambda = 15;
tolFun = 1e-3;
hidden_layer1_size = 8;
hidden_layer2_size = 8;
hidden_layer3_size = 8;

c = 24 * 7 * 4;
maxIter = 250;
maxFunEvals = 10000;
num_outputs = 15;

try
    configFile = arg_list{3};
    config = load(configFile);
    lambda = config(1);
    tolFun = config(2);
    hidden_layer1_size = config(3);
    hidden_layer2_size = config(4);
    hidden_layer3_size = config(5);
catch
end_try_catch

load(fileDat);

[X_ax, mu_ax, sigma_ax] = featureNormalize(X(:,1:20));
[X_ay, mu_ay, sigma_ay] = featureNormalize(X(:,21:40));
[X_az, mu_az, sigma_az] = featureNormalize(X(:,41:60));
[X_gx, mu_gx, sigma_gx] = featureNormalize(X(:,61:80));
[X_gy, mu_gy, sigma_gy] = featureNormalize(X(:,81:100));
[X_gz, mu_gz, sigma_gz] = featureNormalize(X(:,101:120));
[X_s, mu_s, sigma_s] = featureNormalize(X(:,121:125));
[X_t, mu_t, sigma_t] = featureNormalize(X(:,126:126));
X = [X_ax X_ay X_az X_gx X_gy X_gz X_s X_t];
X = [X_ay X_ax X_s X_t X_gz];

Xtrain = X(1:end,1:end);
ytrain = y(1:end,1);
input_layer_size  = size(Xtrain, 2);

tic

function stop = outfun(x,optimValues,state)
    printf("\rIteration %i, Cost %f", optimValues.iter, optimValues.fval);
end

initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer1_size);
initial_Theta2 = randInitializeWeights(hidden_layer1_size, hidden_layer2_size);
initial_Theta3 = randInitializeWeights(hidden_layer2_size, hidden_layer3_size);
initial_Theta4 = randInitializeWeights(hidden_layer3_size, num_outputs);

nn_params = [initial_Theta1(:) ; initial_Theta2(:); initial_Theta3(:); ...
                initial_Theta4(:)];

%%%%% Checking gradient %%%%%

if false

disp("Gradient checking...")

numgrad = computeNumericalGradient( @(nn) nnCostFunction(nn, input_layer_size, hidden_layer1_size, ...
            hidden_layer2_size, hidden_layer3_size, ...
            num_outputs, Xtrain(1:100,:), ytrain(1:100,:), lambda), nn_params);

[J, grad] = nnCostFunction(nn_params, input_layer_size, hidden_layer1_size, ...
            hidden_layer2_size, hidden_layer3_size, ...
            num_outputs, Xtrain(1:100,:), ytrain(1:100,:), lambda);

diff = norm(numgrad-grad)/norm(numgrad+grad);
disp("Difference (usually less than 1e-9)")
disp(diff);

endif

%%%%% Other %%%%%

[J, grad] = nnCostFunction(nn_params, input_layer_size, hidden_layer1_size, ...
            hidden_layer2_size, hidden_layer3_size, ...
            num_outputs, Xtrain, ytrain, lambda);

addpath minFunc/
options.Method = 'lbfgs';
options.tolFun = tolFun;
options.maxIter = maxIter;
options.maxFunEvals = maxFunEvals;
options.display = 'off';


[nn_params, cost] = minFunc( @(p) nnCostFunction(p, ...
      input_layer_size, hidden_layer1_size, hidden_layer2_size, ...
      hidden_layer3_size, num_outputs, ...
      Xtrain, ytrain, lambda),
      nn_params, options);

prev_size = 0;
current_size = hidden_layer1_size * (input_layer_size + 1);

Theta1 = reshape(nn_params((prev_size+1):current_size), ...
hidden_layer1_size, (input_layer_size + 1));

prev_size += current_size;
current_size += hidden_layer2_size * (hidden_layer1_size + 1);

Theta2 = reshape(nn_params((prev_size+1):current_size), ...
hidden_layer2_size, (hidden_layer1_size + 1));

prev_size = current_size;
current_size += hidden_layer3_size * (hidden_layer2_size + 1);

Theta3 = reshape(nn_params((prev_size+1):current_size), ...
hidden_layer3_size, (hidden_layer2_size + 1));

prev_size = current_size;
current_size += num_outputs * (hidden_layer3_size + 1);

Theta4 = reshape(nn_params((prev_size+1):current_size), ...
num_outputs, (hidden_layer3_size + 1));



printf('\n\n')
J
cost

toc

save('-binary', outFile, 'Theta1', 'Theta2', 'Theta3', 'Theta4', ...
    'mu_ax', 'sigma_ax', 'mu_ay', 'sigma_ay', 'mu_az', 'sigma_az', ...
    'mu_gx', 'sigma_gx', 'mu_gy', 'sigma_gy', 'mu_gz', 'sigma_gz', ...
    'mu_s', 'sigma_s', 'mu_t', 'sigma_t')
