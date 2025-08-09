## Introduction
This repository contains source code and artifacts from my research on Agentic AI guided RNA editing with CRISPR-Cas13. I demonstrate how Agentic AI can be used to plan Cas13 experiments and run select tasks autonomously to improve experimentation efficiency and reduce the barrier to entry. The approach I used can be extented to other processes as well.

## Contact
Name: Pragyan Ramamoorthy</br>
Email: Pragyan0314@gmail.com

## Artifacts from UCLA Presentation
- [Slide Deck](https://github.com/PragyanR/agentic_ai_rna_editing/blob/main/artifacts/UCLA_Presentation_Final.pdf)
- [Poster](https://github.com/PragyanR/agentic_ai_rna_editing/blob/main/artifacts/UCLA_Poster_Final.pdf)
- [References](https://github.com/PragyanR/agentic_ai_rna_editing/edit/main/README.md#references)

## Configuration Steps
- Check out the repository
- Install uv, if you don't have it installed
- Initialize uv (uv venv) and activate
- Edit .env file to include your GOOGLE_API_KEY. You can create an API Key using this [link](https://ai.google.dev/gemini-api/docs/models).
- Modify the shell scripts (*.sh files) to reflect your project path
- Run run_all.sh scripts to start the servers and the UI
- Once all servers come up fine, using your browser, launch http://127.0.0.1:5001/

## References
1)	Abudayyeh, O. O., Gootenberg, J. S., Essletzbichler, P., Han, S., Joung, J., Belanto, J. J., Verdine, V., Cox, D. B. T., Kellner, M. J., Regev, A., Lander, E. S., Voytas, D. F., Ting, A. Y., & Zhang, F. (2017). RNA targeting with CRISPR–Cas13. Nature, 550(7675), 280–284. https://doi.org/10.1038/nature24049

2)	Bitesize Bio. (2020, February 25). CRISPR-Cas13: A newbie’s guide. https://bitesizebio.com/64751/crispr-cas13/

3)	Wang, Q., Liu, Y., Zhou, J., Yang, C., Wang, G., Tan, Y., Zhang, Y., Zhou, Z., & Chen, H. (2022). Cas13d: A new molecular scissor for transcriptome engineering. Frontiers in Cell and Developmental Biology, 10, Article 878672. https://doi.org/10.3389/fcell.2022.878672

4)	Aytu BioPharma. (2024). A phase 1, open-label, multiple-cohort, dose-escalation study to evaluate the safety and tolerability of HG202 high-fidelity CRISPR-Cas13 (hfCas13Y) RNA-targeting therapy for neovascular age-related macular degeneration (nAMD) (ClinicalTrials.gov Identifier No. NCT06623279). ClinicalTrials.gov. https://clinicaltrials.gov/study/NCT06623279

5)	Hussain B. (2017, May 18). How CRISPR lets us edit our DNA [Video]. YouTube. https://www.youtube.com/watch?v=E2xXypUuGr8

6) 	Cox, D. B. T., Gootenberg, J. S., Abudayyeh, O. O., Franklin, B., Kellner, M. J., Joung, J., & Zhang, F. (2021). RNA editing with CRISPR-Cas13. Cell Genomics, 1(1), Article 100001. https://doi.org/10.1016/j.xgen.2021.100001

7)	 Konermann, S., Lotfy, P., Brideau, N. J., Oki, J., Shokhirev, M. N., & Hsu, P. D. (2018). Transcriptome engineering with RNA-targeting CRISPR–Cas13. Science, 360(6388), 417–420. https://doi.org/10.1126/science.aaq0180

8)	 Wessels, H. H., Méndez-Mancilla, A., Guo, X., Legut, M., Daniloski, Z., & Sanjana, N. E. (2020). Massively parallel Cas13 screens reveal principles for guide RNA design. Nature Biotechnology, 38(6), 722–727. https://doi.org/10.1038/s41587-020-0456-9

9) 	Jin, Y., Li, R., Qiu, X., Chen, Z., Wu, Y., & Chen, X. (2025). Efficient in silico gRNA design for Cas13 RNA targeting. arXiv. https://arxiv.org/abs/2505.10468

10)	Hou, X., Zhao, Y., Wang, S., & Wang, H. (2025). Model context protocol (MCP): Landscape, security threats, and future  research directions. arXiv. https://arxiv.org/abs/2503.23278

Acknowledgement:
Dr. Vaithi and Team
Coordinators
Guest Speakers

