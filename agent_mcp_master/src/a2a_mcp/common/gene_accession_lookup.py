# type: ignore
"""
Simple Gene Accession Lookup
Get just the RefSeq accession numbers for a gene
"""

import requests
import xml.etree.ElementTree as ET
import time
from typing import List

class SimpleAccessionLookup:
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.tool = "simple_accession_lookup"
    
    def _make_request(self, url: str, params: dict) -> requests.Response:
        """Make request with rate limiting"""
        params.update({'tool': self.tool})
        response = requests.get(url, params=params)
        time.sleep(0.34)  # NCBI rate limit
        return response
    
    def get_accessions(self, gene_symbol: str) -> List[str]:
        """
        Get RefSeq accession numbers for a gene
        
        Args:
            gene_symbol: Gene symbol (e.g., 'BRCA1', 'HNRNPU')
            
        Returns:
            List of accession numbers
        """
        try:
            # Search for RefSeq sequences
            search_url = f"{self.base_url}esearch.fcgi"
            search_params = {
                'db': 'nucleotide',
                'term': f'{gene_symbol}[Gene Name] AND Homo sapiens[Organism] AND RefSeq[Filter]',
                'retmode': 'xml',
                'retmax': '10'
            }
            
            response = self._make_request(search_url, search_params)
            root = ET.fromstring(response.text)
            
            id_list = root.find('.//IdList')
            if id_list is None or len(id_list) == 0:
                return []
            
            ids = [id_elem.text for id_elem in id_list.findall('Id')]
            
            # Get accession numbers
            summary_url = f"{self.base_url}esummary.fcgi"
            summary_params = {
                'db': 'nucleotide',
                'id': ','.join(ids),
                'retmode': 'xml'
            }
            
            response = self._make_request(summary_url, summary_params)
            root = ET.fromstring(response.text)
            
            accessions = []
            for docsum in root.findall('.//DocSum'):
                for item in docsum.findall('Item'):
                    if item.get('Name') == 'AccessionVersion':
                        accessions.append(item.text)
            
            return sorted(accessions)
            
        except Exception:
            return []
    
    def get_mrna_accessions(self, gene_symbol: str) -> List[str]:
        """Get only mRNA (NM_) accessions"""
        all_accessions = self.get_accessions(gene_symbol)
        return [acc for acc in all_accessions if acc.startswith('NM_')]
    
    def get_latest_version(self, base_accession: str) -> str:
        """Get latest version of an accession (e.g., NM_007294 -> NM_007294.4)"""
        try:
            search_url = f"{self.base_url}esearch.fcgi"
            search_params = {
                'db': 'nucleotide',
                'term': base_accession,
                'retmode': 'xml'
            }
            
            response = self._make_request(search_url, search_params)
            root = ET.fromstring(response.text)
            
            id_list = root.find('.//IdList')
            if id_list is None or len(id_list) == 0:
                return ""
            
            uid = id_list.find('Id').text
            
            summary_url = f"{self.base_url}esummary.fcgi"
            summary_params = {
                'db': 'nucleotide',
                'id': uid,
                'retmode': 'xml'
            }
            
            response = self._make_request(summary_url, summary_params)
            root = ET.fromstring(response.text)
            
            docsum = root.find('.//DocSum')
            if docsum is not None:
                for item in docsum.findall('Item'):
                    if item.get('Name') == 'AccessionVersion':
                        return item.text
            
            return ""
            
        except Exception:
            return ""

def main():
    """Example usage"""
    lookup = SimpleAccessionLookup()
    
    # Get all RefSeq accessions for BRCA1
    print("BRCA1 accessions:")
    brca1_accessions = lookup.get_accessions("BRCA1")
    for acc in brca1_accessions:
        print(acc)
        break

if __name__ == "__main__":
    main()
