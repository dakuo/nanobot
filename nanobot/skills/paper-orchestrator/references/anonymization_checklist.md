# Anonymization Checklist (Double-Blind Compliance)

Run this checklist before export. Every item must pass. Any violation blocks submission.

---

## Document Text

- [ ] **Author names removed**: No author names appear anywhere in the paper body, headers, footers, or footnotes.
- [ ] **Self-citations use third-person**: Replace "In our previous work [Smith2023]" with "Smith et al. [Smith2023] showed..." or "[Anonymous Year]" if the cited work would reveal identity.
- [ ] **Institutional affiliations removed**: No university, lab, or company names that would identify the authors appear in the text, acknowledgments, or author bio sections.
- [ ] **Project names anonymized**: No identifiable project names, lab names, or internal tool names that could be traced to the authors.
- [ ] **Grant numbers removed**: No funding agency grant numbers or award IDs in acknowledgments. Use: "This work was supported by [funding agency]" without specific grant numbers.
- [ ] **IRB statement uses generic form**: Replace specific IRB names with: "This study was approved by [anonymous] Institutional Review Board" or "our institution's IRB."

## Figures and Media

- [ ] **No identifiable information in figures**: Screenshots do not show author names, institutional logos, or identifiable URLs.
- [ ] **System screenshots anonymized**: If the system includes author names or institutional branding, blur or replace them.
- [ ] **No watermarks or institutional branding**: Figures are free of university logos, lab watermarks, or corporate branding.
- [ ] **Video/demo links are anonymous**: If supplementary video is provided, host on anonymous platform (not personal YouTube channel). Use anonymous OSF or unlisted links.

## Supplementary Materials

- [ ] **Code repositories are anonymous**: Use Anonymous GitHub (https://anonymous.4open.science/) or anonymous OSF, not personal GitHub accounts.
- [ ] **Datasets are anonymized**: Hosted on anonymous platforms without identifying metadata.
- [ ] **Supplementary PDFs are clean**: No author names in supplementary document text or metadata.

## File Metadata

- [ ] **PDF author field is clean**: PDF document properties do not contain author names, institution, or identifying software tags. Check: File > Properties > Author field should be empty or generic.
- [ ] **PDF creation tool is generic**: If using LaTeX, the default metadata is usually clean. If using Word/Google Docs, manually clear document properties.
- [ ] **Image EXIF data stripped**: Figures exported from personal devices may contain GPS, camera, or author metadata. Strip EXIF before submission.

## References and Citations

- [ ] **Self-citation pattern check**: Verify that self-citations do not form an identifiable cluster. If the paper cites 5+ papers all from the same research group, reviewers may infer authorship. Distribute self-citations among broader related work.
- [ ] **Self-citations in third-person**: Every reference to the authors' own prior work must use third-person: "Zhang et al. [2023] found..." not "We previously showed [Zhang2023]."
- [ ] **[Anonymous] placeholder for unpublished work**: If citing the authors' own under-review or unpublished work, use "[Anonymous, Year]" with a footnote: "Reference removed for double-blind review."
- [ ] **URLs in references**: Personal websites, lab pages, or project URLs that contain author names must be anonymized or replaced with "[URL removed for review]".
- [ ] **Reference list completeness**: Ensure anonymized references still have sufficient bibliographic detail (title, venue, year) for reviewers to locate them.

## Common Gotchas

- [ ] **Acknowledgments section**: Either remove entirely or replace all specifics with generic placeholders: "[Removed for review]".
- [ ] **Appendix materials**: Appendices follow the same anonymization rules as the main paper.
- [ ] **Track changes / comments**: Ensure no revision comments, tracked changes, or editor notes remain visible in the submitted document.
- [ ] **LaTeX comments**: Remove any `%` comments in .tex source that contain author names or identifying information (some submission systems expose source files).
- [ ] **Filename conventions**: Submitted filenames should not contain author names (e.g., `smith_chi2025_final.pdf` violates anonymity).
- [ ] **Formative study participants**: If the paper describes formative work with identifiable collaborators or domain experts, anonymize their descriptions to prevent identification of the research group.
- [ ] **Geographic specificity**: If the study was conducted at a specific, identifiable location (e.g., "the campus clinic at [University X]"), generalize to "a university campus clinic."

---

## Verification Process

1. **Automated text scan**: Search the full paper text for each author's last name, first name, institution name, lab name, and project name. Use case-insensitive matching.
2. **Citation pattern analysis**: Count self-citations (based on author list in `paper_project.yaml`). Flag if any single author group has 5+ citations from the same lab.
3. **Figure visual inspection**: Review all figures, screenshots, and captions for institutional logos, author names, identifiable URLs, or system branding.
4. **Metadata inspection**: Check PDF document properties (Author, Creator, Producer fields). Check image EXIF data for all included figures.
5. **Supplementary materials audit**: Verify anonymous GitHub/OSF links are functional and contain no identifying information in README, commit history, or file metadata.
6. **Cross-reference with author profiles**: Search Google Scholar profiles for each author to check if any unique phrases from the paper appear in their prior work descriptions or project pages.

## Remediation Actions

When a violation is found:
- **Text violations**: Edit the paper to remove or anonymize the identified text.
- **Figure violations**: Re-export figures with identifying information removed or blurred.
- **Metadata violations**: Use `exiftool` to strip EXIF from images; use `pdftk` or LaTeX `\hypersetup{pdfauthor={}}` to clear PDF metadata.
- **Code/data violations**: Re-create anonymous repository links with cleaned content.

If any check fails, the export phase is blocked until the violation is resolved. Re-run the full checklist after remediation to catch any introduced issues.
