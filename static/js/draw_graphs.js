
function CreateLegend(num_gr) {
   // var obj = JSROOT.Create("TLegend"); // only with dev version

   var obj = JSROOT.Create("TPave");
   JSROOT.Create("TAttText", obj);
   JSROOT.extend(obj, { fColumnSeparation: 0, fEntrySeparation: 0.1, fMargin: 0.25, fNColumns: 1, fPrimitives: JSROOT.Create("TList") });
   obj._typename = 'TLegend';
   var xL = 0.6;
   var xR = 0.9;
   var yU = 0.9;
   var dy = 0.04;
   var yD = yU-dy*num_gr;
   JSROOT.extend(obj, { fX1NDC: xL, fY1NDC: yD, fX2NDC: xR, fY2NDC: yU });
//    JSROOT.extend(obj, { fX1NDC: 0.6, fY1NDC:0.75, fX2NDC: 0.9, fY2NDC:0.9 });

   return obj;
}

function CreateLegendEntry(obj, lbl) {
//         var entry = JSROOT.Create("TLegendEntry"); // only with dev version

   var entry = JSROOT.Create("TObject");
   JSROOT.Create("TAttText", entry);
   JSROOT.Create("TAttLine", entry);
   JSROOT.Create("TAttFill", entry);
   JSROOT.Create("TAttMarker", entry);
   JSROOT.extend(entry, { fLabel: "", fObject: null, fOption: "" });
   entry._typename = 'TLegendEntry';

   entry.fObject = obj;
   entry.fLabel = lbl;
   entry.fOption = "lp";
   return entry;
}

function updateGUI(id_obj,xx,yy,num_gr,maxX,minY,maxY,xlabels,xsForLabels,names) {
    // this is just generation of graph
    var graphs_js = [];
    var leg = CreateLegend(num_gr);
    var mgraph = JSROOT.Create("TMultiGraph");
    for (var igr=0; igr<num_gr; igr++) {
        graphs_js[igr] = JSROOT.CreateTGraph(xx[igr].length, xx[igr], yy[igr]);
        var iColor = igr+1;
        if (iColor==10) {iColor += 25;}
        graphs_js[igr].fLineColor = iColor;
        graphs_js[igr].fMarkerColor = iColor;
        graphs_js[igr].fMarkerStyle = 20;
        graphs_js[igr].fMarkerSize = 0.4;
        graphs_js[igr].fName = names[igr];
        mgraph.fGraphs.Add(graphs_js[igr], "lp");
        leg.fPrimitives.Add( CreateLegendEntry(graphs_js[igr], names[igr]) );
    }

    mgraph.fTitle = "";

    //set fixed Y-range
    var delta = maxY-minY;
    if (delta<0.01) {delta=0.01};
    mgraph.fMinimum = minY - 0.5*delta;
    mgraph.fMaximum = maxY + 0.5*delta;

    var h1 = JSROOT.CreateTH1(maxX+1);
    h1.fName = "axis_draw";
    h1.fTitle = "";
    h1.fMinimum = mgraph.fMinimum;
    h1.fMaximum = mgraph.fMaximum;
    h1.fXaxis.fXmin = 0;
    h1.fXaxis.fXmax = maxX;
    h1.fXaxis.fLabelSize = 0.2;
    h1.fXaxis.fLabels = JSROOT.Create("THashList");

    for (var i = 0; i < xsForLabels.length; i++){
        var lbl = JSROOT.Create("TObjString");
        var xlab = xlabels[i];
        lbl.fString = xlab.substr(5);
        lbl.fUniqueID = xsForLabels[i]+1;
        h1.fXaxis.fLabels.Add(lbl, "");
    }
    mgraph.fHistogram = h1;
    mgraph.fFunctions.Add(leg,"");

    JSROOT.redraw(id_obj, mgraph);
}
