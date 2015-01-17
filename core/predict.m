format none

source code.m

arg_list = argv();
fileResult = arg_list{1};
fileXy = arg_list{2};

load(fileResult);
load(fileXy);

X_ax = (X(:,1:20) - mu_ax) ./ sigma_ax;
X_ay = (X(:,21:40) - mu_ay) ./ sigma_ay;
X_az = (X(:,41:60) - mu_az) ./ sigma_az;
X_gx = (X(:,61:80) - mu_gx) ./ sigma_gx;
X_gy = (X(:,81:100) - mu_gy) ./ sigma_gy;
X_gz = (X(:,101:120) - mu_gz) ./ sigma_gz;
X_s = (X(:,121:125) - mu_s) ./ sigma_s;

X = [X_ax X_ay X_az X_gx X_gy X_gz X_s];
X = [X_ay X_ax X_s];

a1 = [ones(size(X)(1),1) X];
z2 = a1 * Theta1';
a2 = sigmoid(z2);
a22 = [ones(size(a2)(1), 1) a2];
z3 = a22 * Theta2';
a3 = h0 = sigmoid(z3);

[dummy, p] = max(h0');

indx = y != 1;

%[y(indx) p'(indx)]
fprintf('\nTraining Set Accuracy For Events Only: %f\n', mean(double(p'(indx) == y(indx))) * 100);

indx = y == 1;

%[y(indx) p'(indx)]
fprintf('\nTraining Set Accuracy For Idle Only: %f\n', mean(double(p'(indx) == y(indx))) * 100);

%[y p']
fprintf('\nTraining Set Accuracy Overall: %f\n', mean(double(p' == y)) * 100);

indx = y == 4;
if sum(y(indx)) > 0
  fprintf('\nAccuracy For Line Change Left: %f, Num %d\n', mean(double(p'(indx) == y(indx))) * 100, sum(y(indx)));
endif

indx = y == 5;
if sum(y(indx)) > 0
  fprintf('\nAccuracy For Line Change Right: %f, Num %d\n', mean(double(p'(indx) == y(indx))) * 100, sum(y(indx)));
endif

indx = y == 6;
if sum(y(indx)) > 0
  fprintf('\nAccuracy For Obstacle Right: %f, Num %d\n', mean(double(p'(indx) == y(indx))) * 100, sum(y(indx)));
endif

indx = y == 7;
if sum(y(indx)) > 0
  fprintf('\nAccuracy For Obstacle Left: %f, Num %d\n', mean(double(p'(indx) == y(indx))) * 100, sum(y(indx)));
endif

indx = y == 8;
if sum(y(indx)) > 0
  fprintf('\nAccuracy For Overtake Right: %f, Num %d\n', mean(double(p'(indx) == y(indx))) * 100, sum(y(indx)));
endif

indx = y == 9;
if sum(y(indx)) > 0
  fprintf('\nAccuracy For Overtake Left: %f, Num %d\n', mean(double(p'(indx) == y(indx))) * 100, sum(y(indx)));
endif

indx = y == 10;
if sum(y(indx)) > 0
  fprintf('\nAccuracy For 45 Right: %f, Num %d\n', mean(double(p'(indx) == y(indx))) * 100, sum(y(indx)));
endif

indx = y == 11;
if sum(y(indx)) > 0
  fprintf('\nAccuracy For 45 Left: %f, Num %d\n', mean(double(p'(indx) == y(indx))) * 100, sum(y(indx)));
endif

indx = y == 12;
if sum(y(indx)) > 0
  fprintf('\nAccuracy For 90 Right: %f, Num %d\n', mean(double(p'(indx) == y(indx))) * 100, sum(y(indx)));
endif

indx = y == 13;
if sum(y(indx)) > 0
  fprintf('\nAccuracy For 90 Left: %f, Num %d\n', mean(double(p'(indx) == y(indx))) * 100, sum(y(indx)));
endif

indx = y == 14;
if sum(y(indx)) > 0
  fprintf('\nAccuracy For 180 Right: %f, Num %d\n', mean(double(p'(indx) == y(indx))) * 100, sum(y(indx)));
endif

indx = y == 15;
if sum(y(indx)) > 0
  fprintf('\nAccuracy For 180 Left: %f, Num %d\n', mean(double(p'(indx) == y(indx))) * 100, sum(y(indx)));
endif
