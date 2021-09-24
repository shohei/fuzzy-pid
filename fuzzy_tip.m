clear; clc; close all;

% fis = mamfis('Name',"tipper");
% 
% fis = addInput(fis,[0 10],'Name',"service");
% fis = addMF(fis,"service","gaussmf",[1.5 0],'Name',"poor");
% fis = addMF(fis,"service","gaussmf",[1.5 5],'Name',"good");
% fis = addMF(fis,"service","gaussmf",[1.5 10],'Name',"excellent");
% 
% fis = addInput(fis,[0 10],'Name',"food");
% fis = addMF(fis,"food","trapmf",[-2 0 1 3],'Name',"rancid");
% fis = addMF(fis,"food","trapmf",[7 9 10 12],'Name',"delicious");
% 
% fis = addOutput(fis,[0 30],'Name',"tip");
% fis = addMF(fis,"tip","trimf",[0 5 10],'Name',"cheap");
% fis = addMF(fis,"tip","trimf",[10 15 20],'Name',"average");
% fis = addMF(fis,"tip","trimf",[20 25 30],'Name',"generous");

fis = mamfis('Name','tipper');

fis.Inputs(1) = fisvar;
fis.Inputs(1).Name = "service";
fis.Inputs(1).Range = [0 10];

fis.Inputs(1).MembershipFunctions(1) = fismf;
fis.Inputs(1).MembershipFunctions(1).Name = "poor";
fis.Inputs(1).MembershipFunctions(1).Type = "gaussmf";
fis.Inputs(1).MembershipFunctions(1).Parameters = [1.5 0];
fis.Inputs(1).MembershipFunctions(2) = fismf;
fis.Inputs(1).MembershipFunctions(2).Name = "good";
fis.Inputs(1).MembershipFunctions(2).Type = "gaussmf";
fis.Inputs(1).MembershipFunctions(2).Parameters = [1.5 5];
fis.Inputs(1).MembershipFunctions(3) = fismf;
fis.Inputs(1).MembershipFunctions(3).Name = "excellent";
fis.Inputs(1).MembershipFunctions(3).Type = "gaussmf";
fis.Inputs(1).MembershipFunctions(3).Parameters = [1.5 10];

fis.Inputs(2) = fisvar([0 10],'Name',"food");
fis.Inputs(2).MembershipFunctions(1) = fismf("trapmf",[-2 0 1 3],...
                                             'Name',"rancid");
fis.Inputs(2).MembershipFunctions(2) = fismf("trapmf",[7 9 10 12],...
                                             'Name',"delicious");
fis.Outputs(1) = fisvar([0 30],'Name',"tip");
mf1 = fismf("trimf",[0 5 10],'Name',"cheap");
mf2 = fismf("trimf",[10 15 20],'Name',"average");
mf3 = fismf("trimf",[20 25 30],'Name',"generous");
fis.Outputs(1).MembershipFunctions = [mf1 mf2 mf3];

ruleList = [1 1 1 1 2;
            2 0 2 1 1;
            3 2 3 1 2];
fis = addRule(fis,ruleList);



evalfis(fis,[1 2])

inputs = [3 5;
          2 7;
          3 1];
evalfis(fis,inputs)

gensurf(fis);
plotmf(fis,'input',1)
plotmf(fis,'output',1)
fis.Rules




















