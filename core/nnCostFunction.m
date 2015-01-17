function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_outputs, ...
                                   X, y, lambda)

Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_outputs, (hidden_layer_size + 1));

trmTheta1 = Theta1(:,[2:end]);
trmTheta2 = Theta2(:,[2:end]);

trTheta1 = trmTheta1(:);
trTheta2 = trmTheta2(:);

m = size(X, 1);
J = 0;

Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));

y_matrix = eye(num_outputs)(y,:);

a1 = [ones(size(X)(1),1) X];
z2 = a1 * Theta1';
a2 = sigmoid(z2);
a22 = [ones(size(a2)(1), 1) a2];
z3 = a22 * Theta2';
a3 = h0 = sigmoid(z3);

j = ((-y_matrix) .* log(h0) - (1 - y_matrix) .* log(1 - h0)) / m;

J = sum(j(:));

J += (sum(trTheta1 .^ 2) + sum(trTheta2 .^ 2)) * (lambda / (2 * m));


% back

b3 = a3 - y_matrix;
b2 = b3 * Theta2(:,[2:end]) .* sigmoidGradient(z2);
% size(Theta1_grad) 25   401
% size(Theta2_grad) 10   26
Theta1_grad = b2' * a1 / m;
Theta2_grad = b3' * a22 / m;
Reg1 = lambda / m * Theta1;
Reg2 = lambda / m * Theta2;

Reg1(:,1) = 0;
Reg2(:,1) = 0;

Theta1_grad += Reg1;
Theta2_grad += Reg2;

end
