#include <time.h>
#include <mysql/mysql.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <vector>
#include <string>
#include <iostream>

#ifndef __CINT__
#include "TROOT.h"
#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TStopwatch.h"
#endif
using namespace std;


extern "C" {
    void treeProcess(const char* fn){
        printf("var fn: %s\n", fn);
        
        FILE *fp = fopen(fn,"r");
        char line[81];
        int cnt=0;
        <vector<string> > sensNames;
        while ( !std::cin.eof(fp) ) {
            sensNames.append(cin.getline())
            cnt++;
        }
        fclose(fp);
        
        printf("----- treeProcess  OK! -----\n");
    }
    TTree* TTree_new() { return new TTree(); }
    void TTree_SetName(TTree* t, const char* name) { 
        printf("----- TTree_SetName: %s\n", name);
        t->SetName(name); 
    }
}

//   TTree *treeSens = new TTree("treeSens","tree for selected sensors");
//   TChain *tree = new TChain("orange");
//   TString dirfileZEUS = "/pnfs/desy.de/dphep/online/zeus/z/ntup/06e/v08b/data/root/";
//   tree->Add(dirfileZEUS+"data_06e_582*.root");
//   TStopwatch t;
//   bool stop=false;
//   t.Start(stop);
//   char d0_out[1000];
//   sprintf(d0_out,"d0_out.root");
//   TFile  f(d0_out,"RECREATE");
//   TTree * ntD0 = new TTree("ntD0", "D0-mesons");
//   ntD0->Branch("Trk_kapx",&D0->Trk_kapx,"trk_kapx/F");
//   ntD0->Branch("Trk_kapy",&D0->Trk_kapy,"trk_kapy/F");
//   ntD0->Branch("Trk_kapz",&D0->Trk_kapz,"trk_kapz/F");
