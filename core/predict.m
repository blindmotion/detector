format none

source code.m

arg_list = argv();
fileTheta1 = arg_list{1};
fileTheta2 = arg_list{2};
fileXy = arg_list{3};

load(fileTheta1);
load(fileTheta2);
load(fileXy);

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
