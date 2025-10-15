from pathlib import Path
import random
import time

from chalkbox import (
    Alert,
    KeyValue,
    Progress,
    Section,
    Spinner,
    Stepper,
    Table,
    get_console,
    setup_logging,
)


class DataImporter:
    """Dataset import orchestrator."""

    def __init__(self, dataset_name: str):
        self.console = get_console()
        self.logger = setup_logging(level="INFO")
        self.dataset_name = dataset_name
        self.download_path = Path.home() / "Downloads" / "datasets"
        self.import_stats = {
            "total_records": 0,
            "imported_records": 0,
            "failed_records": 0,
            "duplicate_records": 0,
        }
        self.validation_errors = []

    def download_dataset(self, url: str, size_mb: int):
        """Download dataset file."""
        self.console.print("\n[bold cyan]Downloading Dataset[/bold cyan]\n")

        download_info = {
            "Dataset": self.dataset_name,
            "URL": url,
            "Size": f"{size_mb} MB",
            "Format": "CSV",
            "Target": str(self.download_path / f"{self.dataset_name}.zip"),
        }

        with Section("Download Information") as section:
            kv = KeyValue(download_info)
            section.add(kv)

        self.console.print()

        # Simulate download
        total_bytes = size_mb * 1024 * 1024

        with Progress() as progress:
            download_task = progress.add_task(
                f"[cyan]Downloading {self.dataset_name}", total=total_bytes
            )

            downloaded = 0
            while downloaded < total_bytes:
                chunk_size = random.randint(100000, 800000)
                chunk_size = min(chunk_size, total_bytes - downloaded)

                time.sleep(0.01)
                downloaded += chunk_size

                progress.update(download_task, advance=chunk_size)

        self.console.print(Alert.success(f"Downloaded {self.dataset_name} ({size_mb} MB)"))

        return True

    def extract_and_validate(self):
        """Extract archive and validate files."""
        self.console.print("\n[bold cyan]📦 Extracting and Validating Files[/bold cyan]\n")

        # Extract
        with Spinner("Extracting archive...") as spinner:
            time.sleep(2)
            spinner.success("Archive extracted")

        # Validate files
        files = [
            {"file": "customers.csv", "records": 10000, "size": "2.5 MB"},
            {"file": "orders.csv", "records": 50000, "size": "15.3 MB"},
            {"file": "products.csv", "records": 5000, "size": "1.2 MB"},
            {"file": "reviews.csv", "records": 25000, "size": "8.7 MB"},
        ]

        validation_results = []

        with Progress() as progress:
            task = progress.add_task("Validating files", total=len(files))

            for file_info in files:
                time.sleep(0.5)

                # Simulate validation
                is_valid = random.random() < 0.95
                _has_header = random.random() < 0.98  # Not used in demo
                encoding = "UTF-8" if random.random() < 0.95 else "ISO-8859-1"

                validation_results.append(
                    {
                        "File": file_info["file"],
                        "Records": f"{file_info['records']:,}",
                        "Size": file_info["size"],
                        "Valid": "✓" if is_valid else "✖",
                        "Encoding": encoding,
                    }
                )

                self.import_stats["total_records"] += file_info["records"]

                if not is_valid:
                    self.validation_errors.append(f"Invalid format in {file_info['file']}")

                progress.update(task, advance=1)

        # Display validation results
        with Section("File Validation Results") as section:
            results_table = Table.from_list_of_dicts(validation_results)
            section.add(results_table)

        if self.validation_errors:
            self.console.print(
                Alert.warning(
                    "Some files have validation warnings",
                    details=f"Found {len(self.validation_errors)} issues",
                )
            )
        else:
            self.console.print(Alert.success("All files validated successfully"))

        return len(self.validation_errors) == 0

    def import_to_database(self):
        """Import data to database."""
        self.console.print("\n[bold cyan]💾 Importing to Database[/bold cyan]\n")

        # Database connection
        with Spinner("Connecting to database...") as spinner:
            time.sleep(1)
            if random.random() < 0.98:
                spinner.success("Connected to database")
            else:
                spinner.error("Database connection failed")
                return False

        # Import tables
        tables = [
            {"name": "customers", "records": 10000, "table": "customer"},
            {"name": "orders", "records": 50000, "table": "order"},
            {"name": "products", "records": 5000, "table": "product"},
            {"name": "reviews", "records": 25000, "table": "review"},
        ]

        import_results = []

        for table_info in tables:
            self.console.print(f"\n[bold]Importing {table_info['name']}...[/bold]")

            with Progress() as progress:
                task = progress.add_task(
                    f"Importing {table_info['table']}", total=table_info["records"]
                )

                imported = 0
                failed = 0
                duplicates = 0
                batch_size = 1000

                while imported < table_info["records"]:
                    batch = min(batch_size, table_info["records"] - imported)

                    # Simulate import with occasional failures
                    time.sleep(random.uniform(0.05, 0.15))

                    # 95% success rate per batch
                    if random.random() < 0.95:
                        imported += batch
                        self.import_stats["imported_records"] += batch
                    else:
                        # Some records fail or are duplicates
                        successful = int(batch * 0.9)
                        dups = int(batch * 0.05)
                        fails = batch - successful - dups

                        imported += successful
                        duplicates += dups
                        failed += fails

                        self.import_stats["imported_records"] += successful
                        self.import_stats["duplicate_records"] += dups
                        self.import_stats["failed_records"] += fails

                    progress.update(task, advance=batch)

            import_results.append(
                {
                    "Table": table_info["table"],
                    "Total": table_info["records"],
                    "Imported": imported,
                    "Duplicates": duplicates,
                    "Failed": failed,
                    "Success Rate": f"{imported/table_info['records']*100:.1f}%",
                }
            )

        # Display import results
        self.console.print("\n")
        with Section("Import Results", subtitle="By Table") as section:
            results_table = Table.from_list_of_dicts(import_results)
            section.add(results_table)

        return True

    def run_data_quality_checks(self):
        """Run data quality checks on imported data."""
        self.console.print("\n[bold cyan]✓ Running Data Quality Checks[/bold cyan]\n")

        quality_checks = [
            "Checking for NULL values",
            "Validating foreign key constraints",
            "Checking data type consistency",
            "Validating date ranges",
            "Checking for outliers",
            "Verifying uniqueness constraints",
        ]

        quality_results = []

        with Progress() as progress:
            task = progress.add_task("Running quality checks", total=len(quality_checks))

            for check in quality_checks:
                time.sleep(random.uniform(0.5, 1))

                # Simulate check results
                issues_found = random.randint(0, 50) if random.random() < 0.3 else 0
                severity = (
                    "error" if issues_found > 20 else "warning" if issues_found > 5 else "success"
                )

                quality_results.append(
                    {
                        "Check": check,
                        "Issues Found": issues_found,
                        "Status": "✖ Failed"
                        if severity == "error"
                        else "⚠ Warning"
                        if severity == "warning"
                        else "✓ Passed",
                    }
                )

                progress.update(task, advance=1)

        # Display quality check results
        with Section("Data Quality Results") as section:
            quality_table = Table(headers=["Check", "Issues Found", "Status"])

            for result in quality_results:
                if "✖" in result["Status"]:
                    severity = "error"
                elif "⚠" in result["Status"]:
                    severity = "warning"
                else:
                    severity = "success"

                quality_table.add_row(
                    result["Check"],
                    str(result["Issues Found"]),
                    result["Status"],
                    severity=severity,
                )

            section.add(quality_table)

        total_issues = sum(r["Issues Found"] for r in quality_results)

        if total_issues > 50:
            self.console.print(
                Alert.error(
                    "Data quality issues detected",
                    details=f"Found {total_issues} total issues requiring attention",
                )
            )
        elif total_issues > 10:
            self.console.print(
                Alert.warning(
                    "Minor data quality issues",
                    details=f"Found {total_issues} issues to review",
                )
            )
        else:
            self.console.print(Alert.success("Data quality checks passed"))

        return total_issues


def run_data_import():
    """Execute data import workflow."""
    console = get_console()

    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]           Dataset Import Workflow[/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]\n")

    # Dataset configuration
    dataset_config = {
        "Name": "ecommerce-dataset-2024",
        "Source": "https://data.example.com/datasets/ecommerce/",
        "Size": "28 MB",
        "Format": "CSV (zipped)",
        "Tables": "4 (customers, orders, products, reviews)",
        "Total Records": "~90,000",
    }

    with Section("Dataset Information") as section:
        kv = KeyValue(dataset_config)
        section.add(kv)

    # Initialize importer
    importer = DataImporter(dataset_config["Name"])

    # Import steps
    steps = [
        "Download dataset",
        "Extract and validate files",
        "Import to database",
        "Run data quality checks",
        "Generate summary report",
    ]

    console.print("\n")
    stepper = Stepper.from_list(steps, title="Import Progress")
    console.print(stepper)

    # Execute import
    start_time = time.time()

    # Step 1: Download
    stepper.start(0)
    if importer.download_dataset(dataset_config["Source"], 28):
        stepper.complete(0)
    else:
        stepper.fail(0, "Download failed")
        return

    # Step 2: Extract and validate
    stepper.start(1)
    validation_ok = importer.extract_and_validate()
    if validation_ok:
        stepper.complete(1)
    else:
        stepper.complete(1)  # Continue with warnings

    # Step 3: Import
    stepper.start(2)
    if importer.import_to_database():
        stepper.complete(2)
    else:
        stepper.fail(2, "Database import failed")
        console.print("\n")
        console.print(stepper)
        return

    # Step 4: Quality checks
    stepper.start(3)
    quality_issues = importer.run_data_quality_checks()
    if quality_issues < 50:
        stepper.complete(3)
    else:
        stepper.fail(3, "Too many quality issues")

    # Step 5: Report
    stepper.start(4)
    with Spinner("Generating summary report...") as spinner:
        time.sleep(1)
        spinner.success("Report generated")
    stepper.complete(4)

    import_time = time.time() - start_time

    # Final summary
    console.print("\n")
    console.print(stepper)

    console.print("\n")
    with Section("Import Summary", subtitle="Complete") as section:
        success_rate = (
            importer.import_stats["imported_records"] / importer.import_stats["total_records"] * 100
        )

        summary = {
            "Import Time": f"{import_time:.1f}s",
            "Total Records": f"{importer.import_stats['total_records']:,}",
            "Imported": f"{importer.import_stats['imported_records']:,}",
            "Failed": f"{importer.import_stats['failed_records']:,}",
            "Duplicates": f"{importer.import_stats['duplicate_records']:,}",
            "Success Rate": f"{success_rate:.1f}%",
            "Quality Issues": quality_issues,
        }

        kv = KeyValue(summary)
        section.add(kv)

        # Show validation errors if any
        if importer.validation_errors:
            section.add_spacing()
            section.add_text("Validation Errors:", style="bold red")
            for error in importer.validation_errors:
                section.add_text(f"  • {error}", style="red")

    # Database statistics
    console.print("\n")
    with Section("Database Statistics") as section:
        db_stats = [
            {"Table": "customer", "Records": "9,850", "Size": "2.4 MB"},
            {"Table": "order", "Records": "48,920", "Size": "14.8 MB"},
            {"Table": "product", "Records": "4,975", "Size": "1.2 MB"},
            {"Table": "review", "Records": "24,680", "Size": "8.5 MB"},
        ]

        stats_table = Table.from_list_of_dicts(db_stats)
        section.add(stats_table)

    # Next steps
    console.print("\n")
    with Section("Next Steps") as section:
        section.add_text("1. Review data quality issues:", style="bold")
        section.add_text("   psql -d mydb -c 'SELECT * FROM data_quality_log'", style="dim cyan")
        section.add_spacing()

        section.add_text("2. Create indexes for performance:", style="bold")
        section.add_text("   python manage.py create_indexes", style="dim cyan")
        section.add_spacing()

        section.add_text("3. Run analytics queries:", style="bold")
        section.add_text("   python scripts/analyze_data.py", style="dim cyan")

    # Final status
    console.print("\n")
    if success_rate >= 95 and quality_issues < 20:
        console.print(
            Alert.success(
                "Data import completed successfully",
                details=f"Imported {importer.import_stats['imported_records']:,} records with high quality",
            )
        )
    elif success_rate >= 90:
        console.print(
            Alert.warning(
                "Data import completed with warnings",
                details=f"Success rate: {success_rate:.1f}%, {quality_issues} quality issues",
            )
        )
    else:
        console.print(
            Alert.error(
                "Data import completed with errors",
                details=f"Low success rate: {success_rate:.1f}%, manual review required",
            )
        )


if __name__ == "__main__":
    run_data_import()
