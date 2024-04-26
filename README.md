# MultiTax

## Description

MultiTax-human is an extensive and high-resolution human-related full-length 16s rRNA reference database, designed to enhance the precision of taxonomic classification in human microbiome research and clinical applications. It integrates over 842,649 high-quality full-length 16S rRNA sequences from multiple public repositories, aiming to provide a detailed portrayal of the human microbiome. Validated across various body parts, MultiTax-human allows for the identification and analysis of core microbial taxa, promoting advances in understanding the microbiome's influence on health and disease. The database also features a user-friendly web interface for easy querying and data exploration.

## Download

The MultiTax reference database and the specialized MultiTax-human database can be downloaded from Google Drive:

- **MultiTax reference database**:
  - Sequence file: `merge_uniques.relabel.fasta` [https://drive.google.com/file/d/1z-V5bUKoUZKwMP1hanGDxJy4N4a6fqOp/view?usp=drive_link](https://drive.google.com/file/d/1z-V5bUKoUZKwMP1hanGDxJy4N4a6fqOp/view?usp=sharing)
  - Index file: `merge_database.udb` [https://drive.google.com/file/d/1ZeTkp_tsOhCQ9xbfwvhdwA_Sj0oh_R0t/view?usp=drive_link](https://drive.google.com/file/d/1ZeTkp_tsOhCQ9xbfwvhdwA_Sj0oh_R0t/view?usp=sharing)
  - Annotation file: `uc_list.tsv` [https://drive.google.com/file/d/1MyAWJBBHcJ5kMvAAdgOLq4CkBusuCVd9/view?usp=drive_link](https://drive.google.com/file/d/1MyAWJBBHcJ5kMvAAdgOLq4CkBusuCVd9/view?usp=sharing)

- **MultiTax-human database**:
  - Sequence file: `merged_human_all.fasta` [https://drive.google.com/file/d/1faElqEKYd-OefOuhB3B36Xwup_6Y9ubz/view?usp=drive_link](https://drive.google.com/file/d/1faElqEKYd-OefOuhB3B36Xwup_6Y9ubz/view?usp=sharing)
  - Index file: `merged_human_all.udb` [https://drive.google.com/file/d/1AzaPpqBILf125iPTebFaqfNxkICJoG5C/view?usp=drive_link](https://drive.google.com/file/d/1AzaPpqBILf125iPTebFaqfNxkICJoG5C/view?usp=sharing)
  - Annotation file: `other_uc_dict_human_anno.tsv` [https://drive.google.com/file/d/17MvIvVnuv3lrmTT_bjLWWudCw8wafQ_k/view?usp=drive_link](https://drive.google.com/file/d/17MvIvVnuv3lrmTT_bjLWWudCw8wafQ_k/view?usp=sharing)

- **MultiTax-human-H120_add database**:
  - Sequence file: `merged_human_all_H120.fasta` https://www.dropbox.com/scl/fi/wzdur7dn07axm682l2oi4/merged_human_all_H120.fasta?rlkey=wnv8ljehkf8z0a4klczwsds6r&dl=0
  - Annotation file: `human_anno_H120_filt.tsv` [https://drive.google.com/file/d/1wISulgkn3AhfT5G5GwRQSwcsTYvw1VYb/view?usp=drive_link](https://drive.google.com/file/d/1wISulgkn3AhfT5G5GwRQSwcsTYvw1VYb/view?usp=sharing)

## Usage Recommendations for Real Samples

Generate a specific amplicon database (V3-V4) using usearch:

```bash
usearch11.0.667_i86linux64 -search_pcr2 merged_human_all_H120.fasta -fwdprimer CCTACGGGNGGCWGCAG -revprimer GACTACHVGGGTATCTAATCC -minamp 400 -maxamp 550 -strand both -fastaout merged_human_all_H120_v34_hits.fa
```

Deduplicate data:

```bash
usearch11.0.667_i86linux64 -fastx_uniques example_sequences.fq -sizeout -relabel UniqueSeqs -fastaout example_sequences_uniq.fa
```

Denoise to generate OTUs:

```bash
usearch11.0.667_i86linux64 -unoise3 example_sequences_uniq.fa -zotus example_sequences_zotus.fa
```

Database alignment:

```bash
usearch11.0.667_i86linux64 -usearch_global example_sequences_zotus.fa -db merged_human_all_H120_v34_hits.fa -maxaccepts 0 -maxrejects 0 -strand both -top_hit_only -id 0 -blast6out example_matches.b6 -threads 75
```

## License

This project is licensed under the MIT License.

## Citation

Please cite the following publication when using MultiTax in your research:

## Contact

For further inquiries or feedback, please contact us at zwbao1996@zju.edu.cn.
