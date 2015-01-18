function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer1_size, ...
                                   hidden_layer2_size, ...
                                   hidden_layer3_size, ...
                                   num_outputs, ...
                                   X, y, lambda)

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

trmTheta1 = Theta1(:,[2:end]);
trmTheta2 = Theta2(:,[2:end]);
trmTheta3 = Theta3(:,[2:end]);
trmTheta4 = Theta4(:,[2:end]);

trTheta1 = trmTheta1(:);
trTheta2 = trmTheta2(:);
trTheta3 = trmTheta3(:);
trTheta4 = trmTheta4(:);

m = size(X, 1);
J = 0;

Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));
Theta3_grad = zeros(size(Theta3));
Theta4_grad = zeros(size(Theta4));

y_matrix = eye(num_outputs)(y,:);

a1 = [ones(size(X)(1),1) X];
z2 = a1 * Theta1';
a2 = sigmoid(z2);
a22 = [ones(size(a2)(1), 1) a2];
z3 = a22 * Theta2';
a3 = sigmoid(z3);
a33 = [ones(size(a3)(1), 1) a3];
z4 = a33 * Theta3';
a4 = sigmoid(z4);
a44 = [ones(size(a4)(1), 1) a4];
z5 = a44 * Theta4';
a5 = sigmoid(z5);

h0 = a5;

j = ((-y_matrix) .* log(h0) - (1 - y_matrix) .* log(1 - h0)) / m;

J = sum(j(:));

J += (sum(trTheta1 .^ 2) + sum(trTheta2 .^ 2) + sum(trTheta3 .^ 2) ...
        + sum(trTheta4 .^ 2)) * (lambda / (2 * m));


% back

b5 = a5 - y_matrix;
b4 = b5 * Theta4(:,[2:end]) .* sigmoidGradient(z4);
b3 = b4 * Theta3(:,[2:end]) .* sigmoidGradient(z3);
b2 = b3 * Theta2(:,[2:end]) .* sigmoidGradient(z2);

Theta1_grad = b2' * a1 / m;
Theta2_grad = b3' * a22 / m;
Theta3_grad = b4' * a33 / m;
Theta4_grad = b5' * a44 / m;
Reg1 = lambda / m * Theta1;
Reg2 = lambda / m * Theta2;
Reg3 = lambda / m * Theta3;
Reg4 = lambda / m * Theta4;

Reg1(:,1) = 0;
Reg2(:,1) = 0;
Reg3(:,1) = 0;
Reg4(:,1) = 0;

Theta1_grad += Reg1;
Theta2_grad += Reg2;
Theta3_grad += Reg3;
Theta4_grad += Reg4;

grad = [Theta1_grad(:) ; Theta2_grad(:); Theta3_grad(:); Theta4_grad(:)];

end
