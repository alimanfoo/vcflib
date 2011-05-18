#include "Variant.h"
#include "split.h"
#include <string>
#include <sstream>
#include <iostream>

using namespace std;
using namespace vcf;

int countAlts(Variant& var, int alleleIndex) {
    int alts = 0;
    for (map<string, map<string, vector<string> > >::iterator s = var.samples.begin(); s != var.samples.end(); ++s) {
        map<string, vector<string> >& sample = s->second;
        map<string, vector<string> >::iterator gt = sample.find("GT");
        if (gt != sample.end()) {
            map<int, int> genotype = decomposeGenotype(gt->second.front());
            for (map<int, int>::iterator g = genotype.begin(); g != genotype.end(); ++g) {
                if (g->first == alleleIndex) {
                    alts += g->second;
                }
            }
        }
    }
    return alts;
}

int main(int argc, char** argv) {

    if (argc != 2) {
        cerr << "usage: " << argv[0] << " <vcf file>" << endl
             << "outputs a VCF stream where AC and NS have been generated for each record using sample genotypes" << endl;
        return 1;
    }

    string filename = argv[1];

    VariantCallFile variantFile;
    if (filename == "-") {
        variantFile.open(std::cin);
    } else {
        variantFile.open(filename);
    }

    if (!variantFile.is_open()) {
        cerr << "could not open " << filename << endl;
        return 1;
    }

    Variant var(variantFile);

    // TODO check if AC is present
    // ensure that AC is listed as an info field
    string line = "##INFO=<ID=AC,Number=A,Type=Integer,Description=\"Total number of alternate alleles in called genotypes\">";
    variantFile.addHeaderLine(line);
    line = "##INFO=<ID=AF,Number=A,Type=Float,Description=\"Estimated allele frequency in the range (0,1]\">";
    variantFile.addHeaderLine(line);
    line = "##INFO=<ID=NS,Number=1,Type=Integer,Description=\"Number of samples with data\">";
    variantFile.addHeaderLine(line);

    // write the new header
    cout << variantFile.header << endl;
 
    // print the records, filtering is done via the setting of varA's output sample names
    while (variantFile.getNextVariant(var)) {
        stringstream ac;
        stringstream ns;
        ns << var.samples.size();
        var.info["NS"].clear();
        var.info["NS"].push_back(ns.str());

        var.info["AC"].clear();
        var.info["AF"].clear();

        for (vector<string>::iterator a = var.alt.begin(); a != var.alt.end(); ++a) {
            string& allele = *a;
            int altcount = countAlts(var, var.getAlleleIndex(allele));
            ac << altcount;
            var.info["AC"].push_back(ac.str());
            stringstream af;
            af << (double) altcount / (double) var.samples.size();
            var.info["AF"].push_back(af.str());
        }
        cout << var << endl;
    }

    return 0;

}
