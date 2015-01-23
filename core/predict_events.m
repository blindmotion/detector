format none
warning("off")

source code.m

THRESHOLD = 0.95;

arg_list = argv();
fileResult = arg_list{1};
fileX = arg_list{2};
fileTime = arg_list{3};
outFileDat = arg_list{4};
outFileTime = arg_list{5};

load(fileResult);
load(fileX);

X_ax = (X(:,1:20) - mu_ax) ./ sigma_ax;
X_ay = (X(:,21:40) - mu_ay) ./ sigma_ay;
X_az = (X(:,41:60) - mu_az) ./ sigma_az;
X_gx = (X(:,61:80) - mu_gx) ./ sigma_gx;
X_gy = (X(:,81:100) - mu_gy) ./ sigma_gy;
X_gz = (X(:,101:120) - mu_gz) ./ sigma_gz;
X_s = (X(:,121:125) - mu_s) ./ sigma_s;
X_t = (X(:,126:126) - mu_t) ./ sigma_t;

X = [X_ay X_ax X_s X_t];

a1 = [ones(size(X)(1),1) X];
z2 = a1 * Theta1';
a2 = sigmoid(z2);
a22 = [ones(size(a2)(1), 1) a2];
z3 = a22 * Theta2';
a3 = h0 = sigmoid(z3);

[prob, y] = max(h0');
y = y';
prob = prob';

indx = prob > THRESHOLD;
y = y(indx);
prob = prob(indx);

t = cell2mat(textread(fileTime, '%s'));
t = t(indx,:);

indx = y != 1;
y = y(indx);
prob = prob(indx);
t = t(indx,:);

csvwrite(outFileDat, [y prob]);
dlmwrite(outFileTime, t, "");