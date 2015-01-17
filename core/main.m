source code.m

format none
warning("off")

arg_list = argv();
fileDat = arg_list{1};

load(fileDat)

%X = X(1:500,:);
%y = y(1:500,:);

[X, mu, sigma] = featureNormalize(X);

X = [X];
%y = Y(1:end,2);
c = 24 * 7 * 4;
Xtrain = X(1:end,1:end);
ytrain = y(1:end,1);
lambda = 100;
maxIter = 120;
tolFun = 1e-5;
input_layer_size  = size(Xtrain, 2);
hidden_layer_size = 64;
num_outputs = 15;

tic

function stop = outfun(x,optimValues,state)
    printf("Iteration %s", disp(optimValues.iter))
    printf("Cost %s \n", disp(optimValues.fval))
end

initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size);
initial_Theta2 = randInitializeWeights(hidden_layer_size, num_outputs);

nn_params = [initial_Theta1(:) ; initial_Theta2(:)];

[J, grad] = nnCostFunction(nn_params, input_layer_size, hidden_layer_size, num_outputs, Xtrain, ytrain, lambda);

options = optimset('MaxIter', maxIter, 'OutputFcn', @outfun, 'TolFun', tolFun);

costFunction = @(p) nnCostFunction(p, ...
                                   input_layer_size, hidden_layer_size, num_outputs, Xtrain, ytrain, lambda);

[nn_params, cost] = fminunc(costFunction, nn_params, options);

Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_outputs, (hidden_layer_size + 1));

J
cost

toc

save theta1.mat Theta1
save theta2.mat Theta2
csvwrite('theta1.csv', Theta1)
csvwrite('theta2.csv', Theta2)
