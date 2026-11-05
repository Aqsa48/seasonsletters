%% Copyright (c) 2026 aqsa. MIT License; see LICENSE.
\NeedsTeXFormat{LaTeX2e}[2020/10/01]
\ProvidesClass{seasonalletter}[2026/11/05 v0.1.0 Personal correspondence]
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[11pt]{article}
\RequirePackage[left=30mm,right=30mm,top=45mm,bottom=35mm]{geometry}
\RequirePackage[T1]{fontenc}
\RequirePackage{mathpazo}
\RequirePackage{seasonalletters}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{.8em}
\endinput
