arg_list = argv();
inFile = arg_list{1};
outFile = arg_list{2};

data = load(inFile);
y = data(:,1);
X = data(:,2:end);

save('-binary', outFile, 'X', 'y')
