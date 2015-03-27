format none
warning("off")

source code.m

THRESHOLD = 0.92;

arg_list = argv();
fileX = arg_list{1};
fileTime = arg_list{2};
outFileDat = arg_list{3};
outFileTime = arg_list{4};

thetas = [];

try
    arg_cursor = 5;
    while true
        thetas = [thetas; arg_list{arg_cursor}];
        arg_cursor += 1;
    endwhile
catch
end_try_catch

ys = [];
probs = [];

for i = 1:size(thetas)
    theta = thetas(i,:)
    load(fileX);
    load(theta);

    X_ax = (X(:,1:20) - mu_ax) ./ sigma_ax;
    X_ay = (X(:,21:40) - mu_ay) ./ sigma_ay;
    X_az = (X(:,41:60) - mu_az) ./ sigma_az;
    X_gx = (X(:,61:80) - mu_gx) ./ sigma_gx;
    X_gy = (X(:,81:100) - mu_gy) ./ sigma_gy;
    X_gz = (X(:,101:120) - mu_gz) ./ sigma_gz;
    X_s = (X(:,121:125) - mu_s) ./ sigma_s;
    X_t = (X(:,126:126) - mu_t) ./ sigma_t;

    X = [X_ay X_ax X_s X_t X_gz];

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

    h0(:,12) = h0(:,12) * 1.1;
    h0(:,13) = h0(:,13) * 1.1;

    [prob, y] = max(h0');
    y = y';
    prob = prob';

    ys = [ys y];
    probs = [probs prob];
endfor

if size(ys,2) == 1
    ys = [ys ys];
endif

prob = mean(probs,2);

indx1 = mean(ys,2) == ys(:,1);
indx2 = std(ys')' == zeros(size(ys,1),1);
indx3 = prob > THRESHOLD;
indx = indx1 & indx2 & indx3;

y = ys(indx,1);
prob = prob(indx);

t = cell2mat(textread(fileTime, '%s'));
t = t(indx,:);

indx = y != 1;
y = y(indx);
prob = prob(indx);
t = t(indx,:);

csvwrite(outFileDat, [y prob]);
dlmwrite(outFileTime, t, "");
