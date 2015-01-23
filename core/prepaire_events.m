arg_list = argv();
inFile = arg_list{1};
outFile = arg_list{2};

data = load(inFile);
X = data;

save('-binary', outFile, 'X')
