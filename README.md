<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">

# IDX_FINANCIAL_REPORT

<em></em>

<!-- BADGES -->
<img src="https://img.shields.io/github/license/Rachdyan/idx_financial_report?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
<img src="https://img.shields.io/github/last-commit/Rachdyan/idx_financial_report?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/Rachdyan/idx_financial_report?style=default&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/Rachdyan/idx_financial_report?style=default&color=0080ff" alt="repo-language-count">

<!-- default option, no dependency badges. -->


<!-- default option, no dependency badges. -->

</div>
<br>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
    - [Project Index](#project-index)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)


---

## Background
For investors, analysts, and researchers, gathering and analyzing financial data from publicly listed companies on the Indonesia Stock Exchange (IDX) is a critical yet often tedious process. Manually downloading, extracting, and combining data from numerous financial reports consumes a significant amount of time and effort.

While several services and websites provide aggregated financial data, they often come with their own set of limitations:

- Normalized and Opaque Data: The data provided is typically normalized according to the service's internal standards. This can obscure the nuances and specific details present in the company's original financial statements, making it less representative of the raw figures.
- Lack of Data Exportability: Many of these platforms do not allow users to export the raw data. This restricts the ability to perform custom, in-depth analysis and exploration using your own tools and methodologies.

This project aims to solve these problems by providing a tool to directly scrape financial report data from the source, ensuring that the data is raw, unfiltered, and readily available for your own analytical needs


---

## Features

- Automated scraping and combining of financial reports from [idx.co.id](https://www.idx.co.id)
- Supports quarterly dan annual financial statements
- Outputs clean Excel files with structured data
- Configurable date range filtering

---

## Project Structure

```sh
└── idx_financial_report/
    ├── data
    ├── get_financial_report.ipynb
    ├── result
    ├── schema
    ├── template
    └── utils
```

### Project Index

<details open>
	<summary><b><code>IDX_FINANCIAL_REPORT/</code></b></summary>
	<!-- __root__ Submodule -->
	<details>
		<summary><b>__root__</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ __root__</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Rachdyan/idx_financial_report/blob/master/get_financial_report.ipynb'>get_financial_report.ipynb</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- utils Submodule -->
	<details>
		<summary><b>utils</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ utils</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Rachdyan/idx_financial_report/blob/master/utils/excel_handler.py'>excel_handler.py</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Rachdyan/idx_financial_report/blob/master/utils/ordered_name.py'>ordered_name.py</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Rachdyan/idx_financial_report/blob/master/utils/download_handler.py'>download_handler.py</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Rachdyan/idx_financial_report/blob/master/utils/xbrl_handler.py'>xbrl_handler.py</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
			</table>
		</blockquote>
	</details>
</details>

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python

### Installation

Build idx_financial_report from the source and intsall dependencies:

1. **Clone the repository:**

    ```sh
    ❯ git clone https://github.com/Rachdyan/idx_financial_report
    ```

2. **Navigate to the project directory:**

    ```sh
    ❯ cd idx_financial_report
    ```

3. **Install the dependencies:**

    ```sh
    ❯ pip install -r requirements.txt
    ```

### Usage

Launch the notebook with:

    
    ❯ jupyter notebook get_financial_report.ipynb
    

---

## 🌐 Data Source

Official IDX Financial Reports Portal:
https://www.idx.co.id/primary/ListedCompany/FinancialReport


---

## Roadmap

- [ ] **`Task 1`**: Add support for other industries (Propreti, Infrastruktur, Financing, Asuransi, Sekuritas).

---

## Contributing

- **💬 [Join the Discussions](https://github.com/Rachdyan/idx_financial_report/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/Rachdyan/idx_financial_report/issues)**: Submit bugs found or log feature requests for the `idx_financial_report` project.
- **💡 [Submit Pull Requests](https://github.com/Rachdyan/idx_financial_report/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/Rachdyan/idx_financial_report
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/Rachdyan/idx_financial_report/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=Rachdyan/idx_financial_report">
   </a>
</p>
</details>

---

## License

Idx_financial_report is protected under the [MIT](https://choosealicense.com/licenses/mit/) License. For more details, refer to the [MIT](https://choosealicense.com/licenses/mit/) file.

---

## Disclaimer

This tool is for educational purposes only. Always verify data with official sources before making financial decisions. The maintainers are not responsible for data accuracy or usage consequences.

<div align="right">

[![][back-to-top]](#top)

</div>


[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square


---
