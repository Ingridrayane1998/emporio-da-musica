"""Módulo de perfilamento (profiling) dos arquivos CSV brutos em data/raw."""

from pathlib import Path
from typing import Any

import pandas as pd


def profile_csv(file_path: Path) -> dict[str, Any]:
    """Analisa um arquivo CSV e extrai estatísticas, tipos, nulos e duplicatas."""
    df = pd.read_csv(file_path)

    profile_data = {
        "file_name": file_path.name,
        "rows": len(df),
        "columns_count": len(df.columns),
        "columns": list(df.columns),
        "duplicates": int(df.duplicated().sum()),
        "columns_detail": {},
    }

    for col in df.columns:
        series = df[col]
        null_count = int(series.isna().sum())
        unique_count = int(series.nunique(dropna=True))

        sample_values = series.dropna().head(3).tolist()

        profile_data["columns_detail"][col] = {
            "dtype": str(series.dtype),
            "nulls": null_count,
            "null_pct": round((null_count / len(df)) * 100, 2) if len(df) > 0 else 0,
            "unique": unique_count,
            "sample_values": sample_values,
        }

    return profile_data


def run_all_profiles(raw_dir: Path) -> dict[str, dict[str, Any]]:
    """Executa o perfilamento em todos os CSVs presentes no diretório raw."""
    results = {}
    csv_files = sorted(raw_dir.glob("*.csv"))

    for csv_file in csv_files:
        results[csv_file.name] = profile_csv(csv_file)

    return results


def format_markdown_report(profiles: dict[str, dict[str, Any]]) -> str:
    """Gera um relatório completo em Markdown para inclusão no dicionario_de_dados.md."""
    lines = [
        "# Dicionário de Dados e Relatório de Perfilamento - Empório da Música",
        "",
        "Relatório gerado automaticamente pelo script `src/emporio_ozzy/etl/profile.py`.",
        "",
        "## Resumo Geral das Tabelas",
        "",
        "| Arquivo | Total de Linhas | Colunas | Duplicadas |",
        "| :--- | :--- | :--- | :--- |",
    ]

    for fname, data in profiles.items():
        lines.append(
            f"| `{fname}` | {data['rows']} | {data['columns_count']} | {data['duplicates']} |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Detalhamento por Tabela")
    lines.append("")

    for fname, data in profiles.items():
        lines.append(f"### Tabela: `{fname}`")
        lines.append(f"- **Total de Registros:** {data['rows']}")
        lines.append(f"- **Linhas Duplicadas:** {data['duplicates']}")
        lines.append("")
        lines.append("| Coluna Original | Tipo Inferido | Nulos (%) | Valores Únicos | Amostras |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")

        for col, detail in data["columns_detail"].items():
            samples_str = ", ".join([str(v) for v in detail["sample_values"][:3]])
            lines.append(
                f"| `{col}` | `{detail['dtype']}` | {detail['nulls']} ({detail['null_pct']}%) | "
                f"{detail['unique']} | `{samples_str}` |"
            )

        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    raw_path = Path("data/raw")
    reports = run_all_profiles(raw_path)
    md_content = format_markdown_report(reports)
    print(md_content)

