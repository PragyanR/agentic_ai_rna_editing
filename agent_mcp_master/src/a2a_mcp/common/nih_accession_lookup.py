# type: ignore
"""
NIH/NCBI Accession Lookup Tool
Fetches gene/sequence information using accession numbers from NCBI databases
"""

import requests
import xml.etree.ElementTree as ET
import time
import re
import json


class NCBILookup:
    def __init__(self):
        """
        Initialize NCBI lookup tool
        
        """
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.tool = "python_ncbi_lookup"
        
    def _make_request(self, url: str, params: dict) -> requests.Response:
        """Make request to NCBI with rate limiting"""
        params.update({

            'tool': self.tool
        })
        
        response = requests.get(url, params=params)
        time.sleep(0.34)  # NCBI rate limit: 3 requests per second
        
        if response.status_code != 200:
            raise Exception(f"NCBI API error: {response.status_code}")
            
        return response
    
    def get_sequence_info(self, accession: str, return_json: bool = True) -> str:
        """
        Get basic information about a sequence using accession number
        
        Args:
            accession: RefSeq accession number (e.g., 'NM_031844')
            return_json: If True, returns JSON string; if False, returns dict
            
        Returns:
            JSON string containing sequence information
        """
        print("In get_sequence_info")
        # Search for the accession to get the ID
        search_url = f"{self.base_url}esearch.fcgi"
        search_params = {
            'db': 'nucleotide',
            'term': accession,
            'retmode': 'xml'
        }
        
        search_response = self._make_request(search_url, search_params)
        search_root = ET.fromstring(search_response.text)
        
        id_list = search_root.find('.//IdList')
        if id_list is None or len(id_list) == 0:
            result = {'error': f'No results found for accession {accession}'}
            return json.dumps(result, indent=2) if return_json else result
        
        uid = id_list.find('Id').text
        
        # Fetch detailed information
        fetch_url = f"{self.base_url}efetch.fcgi"
        fetch_params = {
            'db': 'nucleotide',
            'id': uid,
            'rettype': 'gb',
            'retmode': 'xml'
        }
        
        fetch_response = self._make_request(fetch_url, fetch_params)
        
        result = self._parse_genbank_xml(fetch_response.text, accession)
        return json.dumps(result, indent=2) if return_json else result
    
    def get_fasta_sequence(self, accession: str, return_json: bool = True) -> str:
        """
        Get FASTA sequence for given accession
        
        Args:
            accession: RefSeq accession number
            return_json: If True, returns JSON string; if False, returns plain FASTA
            
        Returns:
            JSON string with FASTA sequence or plain FASTA string
        """
        # Search for the accession
        search_url = f"{self.base_url}esearch.fcgi"
        search_params = {
            'db': 'nucleotide',
            'term': accession,
            'retmode': 'xml'
        }
        
        search_response = self._make_request(search_url, search_params)
        search_root = ET.fromstring(search_response.text)
        
        id_list = search_root.find('.//IdList')
        if id_list is None or len(id_list) == 0:
            error_msg = f"Error: No results found for accession {accession}"
            if return_json:
                return json.dumps({"error": error_msg}, indent=2)
            return error_msg
        
        uid = id_list.find('Id').text
        
        # Fetch FASTA sequence
        fetch_url = f"{self.base_url}efetch.fcgi"
        fetch_params = {
            'db': 'nucleotide',
            'id': uid,
            'rettype': 'fasta',
            'retmode': 'text'
        }
        
        fetch_response = self._make_request(fetch_url, fetch_params)
        fasta_content = fetch_response.text
        
        if return_json:
            # Parse FASTA to extract header and sequence
            lines = fasta_content.strip().split('\n')
            if lines and lines[0].startswith('>'):
                header = lines[0]
                sequence = ''.join(lines[1:])
                result = {
                    "accession": accession,
                    "fasta_header": header,
                    "sequence": sequence,
                    "sequence_length": len(sequence)
                }
                return json.dumps(result, indent=2)
            else:
                return json.dumps({"error": "Invalid FASTA format received"}, indent=2)
        
        return fasta_content
    
    def get_gene_info(self, gene_symbol: str, return_json: bool = True) -> str:
        """
        Get gene information by gene symbol
        
        Args:
            gene_symbol: Gene symbol (e.g., 'HNRNPU')
            return_json: If True, returns JSON string; if False, returns list of dicts
            
        Returns:
            JSON string containing gene information
        """
        search_url = f"{self.base_url}esearch.fcgi"
        search_params = {
            'db': 'gene',
            'term': f'{gene_symbol}[Gene Name] AND Homo sapiens[Organism]',
            'retmode': 'xml'
        }
        
        search_response = self._make_request(search_url, search_params)
        search_root = ET.fromstring(search_response.text)
        
        id_list = search_root.find('.//IdList')
        if id_list is None or len(id_list) == 0:
            result = [{'error': f'No gene found for symbol {gene_symbol}'}]
            return json.dumps(result, indent=2) if return_json else result
        
        results = []
        for gene_id in id_list.findall('Id'):
            uid = gene_id.text
            
            # Fetch gene details
            fetch_url = f"{self.base_url}efetch.fcgi"
            fetch_params = {
                'db': 'gene',
                'id': uid,
                'retmode': 'xml'
            }
            
            fetch_response = self._make_request(fetch_url, fetch_params)
            gene_info = self._parse_gene_xml(fetch_response.text)
            results.append(gene_info)
        
        return json.dumps(results, indent=2) if return_json else results
    
    def _parse_genbank_xml(self, xml_content: str, accession: str) -> dict:
        """Parse GenBank XML response"""
        try:
            root = ET.fromstring(xml_content)
            
            # Find the GBSeq element
            gb_seq = root.find('.//GBSeq')
            if gb_seq is None:
                return {'error': 'Invalid XML response'}
            
            info = {
                'accession': accession,
                'version': gb_seq.find('GBSeq_accession-version').text if gb_seq.find('GBSeq_accession-version') is not None else 'N/A',
                'definition': gb_seq.find('GBSeq_definition').text if gb_seq.find('GBSeq_definition') is not None else 'N/A',
                'length': gb_seq.find('GBSeq_length').text if gb_seq.find('GBSeq_length') is not None else 'N/A',
                'organism': gb_seq.find('GBSeq_organism').text if gb_seq.find('GBSeq_organism') is not None else 'N/A',
                'taxonomy': gb_seq.find('GBSeq_taxonomy').text if gb_seq.find('GBSeq_taxonomy') is not None else 'N/A',
                'create_date': gb_seq.find('GBSeq_create-date').text if gb_seq.find('GBSeq_create-date') is not None else 'N/A',
                'update_date': gb_seq.find('GBSeq_update-date').text if gb_seq.find('GBSeq_update-date') is not None else 'N/A'
            }
            
            return info
            
        except ET.ParseError as e:
            return {'error': f'XML parsing error: {str(e)}'}
    
    def _parse_gene_xml(self, xml_content: str) -> dict:
        """Parse Gene XML response"""
        try:
            root = ET.fromstring(xml_content)
            
            # Extract basic gene information
            gene_info = {
                'gene_id': 'N/A',
                'symbol': 'N/A',
                'description': 'N/A',
                'chromosome': 'N/A',
                'map_location': 'N/A',
                'gene_type': 'N/A'
            }
            
            # This is a simplified parser - the actual Gene XML structure is complex
            # You may need to adjust based on the specific XML structure returned
            
            return gene_info
            
        except ET.ParseError as e:
            return {'error': f'XML parsing error: {str(e)}'}

def main():
    """Example usage of the NCBI lookup tool with JSON output"""
    
    # Initialize the lookup tool 
    ncbi = NCBILookup()
    
    # Example 1: Look up HNRNPU sequence information as JSON
    print("=== HNRNPU Sequence Information (JSON) ===")
    hnrnpu_json = ncbi.get_sequence_info("NM_031844.3", return_json=True)
    print(hnrnpu_json)
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Get FASTA sequence as JSON
    print("=== FASTA Sequence (JSON format) ===")
    fasta_json = ncbi.get_fasta_sequence("NM_031844.3", return_json=True)
    print(fasta_json)

    
  

if __name__ == "__main__":
    main()
