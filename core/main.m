source code.m

format none
warning("off")

arg_list = argv();
fileDat = arg_list{1};

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

c = 24 * 7 * 4;
Xtrain = X(1:end,1:end);
ytrain = y(1:end,1);
lambda = 15;
maxIter = 10000;
tolFun = 1e-7;
input_layer_size  = size(Xtrain, 2);
hidden_layer1_size = 8;
hidden_layer2_size = 8;
hidden_layer3_size = 8;
num_outputs = 15;

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

[J, grad] = nnCostFunction(nn_params, input_layer_size, hidden_layer1_size, ...
            hidden_layer2_size, hidden_layer3_size, ...
            num_outputs, Xtrain, ytrain, lambda);

options = optimset('MaxIter', maxIter, 'OutputFcn', @outfun, 'TolFun', tolFun,
    'GradObj', 'on');

costFunction = @(p) nnCostFunction(p, ...
                    input_layer_size, hidden_layer1_size, hidden_layer2_size, ...
                    hidden_layer3_size, num_outputs, ...
                    Xtrain, ytrain, lambda);

[nn_params, cost] = fminunc(costFunction, nn_params, options);



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

save result.mat Theta1 Theta2 Theta3 Theta4 ...
            mu_ax sigma_ax mu_ay sigma_ay mu_az sigma_az ...
            mu_gx sigma_gx mu_gy sigma_gy mu_gz sigma_gz mu_s sigma_s ...
            mu_t sigma_t
