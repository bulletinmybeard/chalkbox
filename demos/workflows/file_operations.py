from datetime import datetime
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
)


class FileProcessor:
    """Simulated batch file processor."""

    def __init__(self):
        self.console = get_console()
        self.processed_files = []
        self.failed_files = []
        self.skipped_files = []
        self.stats = {
            "total_size": 0,
            "processed_size": 0,
            "processing_time": 0,
            "compression_ratio": 0,
        }

    def scan_directory(self, path, extensions=None):
        """Scan directory for files to process."""
        self.console.print("\n[bold cyan]📁 Scanning Directory[/bold cyan]\n")

        # Simulate file discovery
        mock_files = []

        with Spinner(f"Scanning {path}...") as spinner:
            time.sleep(1.5)

            # Generate mock file list
            file_types = {
                ".txt": (10, 100),  # 10-100 KB
                ".csv": (100, 5000),  # 100KB-5MB
                ".json": (1, 500),  # 1-500 KB
                ".log": (50, 10000),  # 50KB-10MB
                ".xml": (10, 1000),  # 10KB-1MB
                ".pdf": (100, 20000),  # 100KB-20MB
                ".jpg": (500, 5000),  # 500KB-5MB
                ".png": (100, 3000),  # 100KB-3MB
            }

            for ext, (min_kb, max_kb) in file_types.items():
                if extensions and ext not in extensions:
                    continue

                # Generate 2-5 files of each type
                count = random.randint(2, 5)
                for _i in range(count):
                    size = random.randint(min_kb, max_kb) * 1024
                    mock_files.append(
                        {
                            "name": f"file_{random.randint(1000, 9999)}{ext}",
                            "path": f"{path}/subdir_{random.randint(1, 3)}",
                            "type": ext[1:].upper(),
                            "size": size,
                            "modified": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "status": "pending",
                        }
                    )

            spinner.success(f"Found {len(mock_files)} files")

        # Display file summary
        with Section("Files Found", subtitle=f"Directory: {path}") as section:
            # Group by type
            type_summary = {}
            for file in mock_files:
                file_type = file["type"]
                if file_type not in type_summary:
                    type_summary[file_type] = {"count": 0, "total_size": 0}
                type_summary[file_type]["count"] += 1
                type_summary[file_type]["total_size"] += file["size"]

            summary_data = []
            for file_type, data in type_summary.items():
                summary_data.append(
                    {
                        "Type": file_type,
                        "Count": data["count"],
                        "Total Size": f"{data['total_size'] / 1024 / 1024:.1f} MB",
                    }
                )

            table = Table.from_list_of_dicts(summary_data)
            section.add(table)

            section.add_spacing()

            total_size = sum(f["size"] for f in mock_files)
            section.add_text(f"Total files: {len(mock_files)}", style="bold")
            section.add_text(f"Total size: {total_size / 1024 / 1024:.1f} MB", style="bold")

        return mock_files

    def validate_files(self, files):
        """Validate files before processing."""
        self.console.print("\n[bold cyan]✓  Validating Files[/bold cyan]\n")

        validated = []
        invalid = []

        with Progress() as progress:
            task = progress.add_task("Validating files", total=len(files))

            for file in files:
                time.sleep(0.1)

                # Simulate validation checks
                checks = {
                    "exists": random.random() < 0.98,
                    "readable": random.random() < 0.95,
                    "not_corrupted": random.random() < 0.97,
                    "size_ok": file["size"] < 50 * 1024 * 1024,  # Max 50MB
                }

                if all(checks.values()):
                    validated.append(file)
                else:
                    invalid.append(file)
                    failed_check = next(k for k, v in checks.items() if not v)
                    file["error"] = f"Validation failed: {failed_check}"

                progress.update(task, advance=1)

        if invalid:
            self.console.print(
                Alert.warning(
                    f"{len(invalid)} files failed validation", details="These files will be skipped"
                )
            )

            # Show invalid files
            with Section("Invalid Files") as section:
                for file in invalid[:5]:  # Show first 5
                    section.add_text(
                        f"• {file['name']}: {file.get('error', 'Unknown error')}", style="yellow"
                    )
                if len(invalid) > 5:
                    section.add_text(f"... and {len(invalid) - 5} more", style="dim")

        return validated

    def process_file(self, file, progress_tracker=None, task_id=None):
        """Process a single file."""
        processing_steps = [
            ("Reading", 0.2),
            ("Analyzing", 0.3),
            ("Transforming", 0.4),
            ("Compressing", 0.3),
            ("Writing", 0.2),
        ]

        start_time = time.time()

        for step_name, duration in processing_steps:
            if progress_tracker and task_id:
                progress_tracker.update(task_id, description=f"{file['name']}: {step_name}...")

            time.sleep(duration * random.uniform(0.5, 1.5))

        # Simulate processing results
        if random.random() < 0.9:  # 90% success rate
            # Success
            processing_time = time.time() - start_time
            compressed_size = int(file["size"] * random.uniform(0.3, 0.7))

            result = {
                "status": "success",
                "original_size": file["size"],
                "compressed_size": compressed_size,
                "compression_ratio": f"{(1 - compressed_size/file['size']) * 100:.1f}%",
                "processing_time": f"{processing_time:.2f}s",
            }

            self.processed_files.append(file)
            self.stats["processed_size"] += file["size"]
            self.stats["processing_time"] += processing_time

            return result
        else:
            # Failure
            error_messages = [
                "Unsupported format",
                "Corruption detected",
                "Insufficient memory",
                "Write permission denied",
            ]

            self.failed_files.append(file)

            return {"status": "failed", "error": random.choice(error_messages)}

    def process_batch(self, files, parallel=4):
        """Process files in batch with parallel simulation."""
        self.console.print("\n[bold cyan] Processing Files[/bold cyan]\n")

        results = []

        with Progress() as progress:
            # Create overall progress
            overall_task = progress.add_task("[bold cyan]Overall Progress", total=len(files))

            # Create tasks for parallel processing
            active_tasks = {}
            completed = 0

            file_queue = files.copy()

            while completed < len(files):
                # Start new tasks if slots available
                while len(active_tasks) < parallel and file_queue:
                    file = file_queue.pop(0)
                    task_id = progress.add_task(f"{file['name']}", total=100)
                    active_tasks[task_id] = {"file": file, "progress": 0, "start_time": time.time()}

                # Update active tasks
                completed_in_cycle = []
                for task_id, task_data in active_tasks.items():
                    # Simulate progress
                    task_data["progress"] += random.randint(10, 30)

                    if task_data["progress"] >= 100:
                        # Task complete
                        progress.update(task_id, completed=100)

                        # Process the file
                        result = self.process_file(task_data["file"])
                        results.append({"file": task_data["file"]["name"], **result})

                        completed_in_cycle.append(task_id)
                        completed += 1
                        progress.update(overall_task, advance=1)
                    else:
                        progress.update(task_id, completed=task_data["progress"])

                # Remove completed tasks
                for task_id in completed_in_cycle:
                    progress.remove_task(task_id)
                    del active_tasks[task_id]

                time.sleep(0.1)

        return results

    def generate_report(self, results):
        """Generate processing report."""
        self.console.print("\n[bold cyan]Processing Report[/bold cyan]\n")

        # Calculate statistics
        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] == "failed"]

        with Section(
            "Processing Summary", subtitle=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ) as section:
            # Overall stats
            overall_stats = {
                "Total Files": len(results),
                "Successful": f"{len(successful)} ({len(successful)/len(results)*100:.1f}%)",
                "Failed": f"{len(failed)} ({len(failed)/len(results)*100:.1f}%)",
                "Total Processing Time": f"{self.stats['processing_time']:.1f}s",
                "Average Time per File": f"{self.stats['processing_time']/len(results):.2f}s",
            }

            kv = KeyValue(overall_stats)
            section.add(kv)

            if successful:
                section.add_spacing()
                section.add_text("Compression Statistics:", style="bold")

                total_original = sum(r["original_size"] for r in successful)
                total_compressed = sum(r["compressed_size"] for r in successful)

                compression_stats = {
                    "Original Total Size": f"{total_original / 1024 / 1024:.1f} MB",
                    "Compressed Total Size": f"{total_compressed / 1024 / 1024:.1f} MB",
                    "Space Saved": f"{(total_original - total_compressed) / 1024 / 1024:.1f} MB",
                    "Average Compression": f"{(1 - total_compressed/total_original) * 100:.1f}%",
                }

                kv = KeyValue(compression_stats)
                section.add(kv)

            if failed:
                section.add_spacing()
                section.add_text("Failed Files:", style="bold red")

                # Group failures by error
                error_groups = {}
                for failure in failed:
                    error = failure.get("error", "Unknown")
                    if error not in error_groups:
                        error_groups[error] = []
                    error_groups[error].append(failure["file"])

                for error, files in error_groups.items():
                    section.add_text(f"  {error}: {len(files)} files", style="red")


def run_file_processor():
    """Run the file processor demonstration."""
    console = get_console()

    console.print("[bold magenta]╔════════════════════════════════════════════╗[/bold magenta]")
    console.print("[bold magenta]║       Batch File Processor v2.0            ║[/bold magenta]")
    console.print("[bold magenta]╚════════════════════════════════════════════╝[/bold magenta]\n")

    processor = FileProcessor()

    config = {
        "source_directory": "/data/incoming",
        "output_directory": "/data/processed",
        "parallel_workers": 4,
        "max_file_size": "50 MB",
        "supported_formats": "txt, csv, json, log, xml",
        "compression": "gzip",
    }

    with Section("Processor Configuration") as section:
        kv = KeyValue(config)
        section.add(kv)

    steps = [
        "Scan directory",
        "Validate files",
        "Process files",
        "Generate report",
        "Archive originals",
    ]

    stepper = Stepper.from_list(steps, title="Processing Pipeline")
    console.print("\n")
    console.print(stepper)

    stepper.start(0)
    files = processor.scan_directory(
        "/data/incoming", extensions=[".txt", ".csv", ".json", ".log", ".xml"]
    )
    stepper.complete(0)

    if not files:
        console.print(Alert.warning("No files found to process"))
        return

    # Step 2: Validate files
    stepper.start(1)
    valid_files = processor.validate_files(files)
    stepper.complete(1)

    if not valid_files:
        console.print(Alert.error("No valid files to process"))
        return

    # Step 3: Process files
    stepper.start(2)
    results = processor.process_batch(valid_files, parallel=4)
    stepper.complete(2)

    # Step 4: Generate report
    stepper.start(3)
    processor.generate_report(results)
    stepper.complete(3)

    # Step 5: Archive originals
    stepper.start(4)
    with Spinner("Archiving original files...") as spinner:
        time.sleep(2)
        spinner.success("Original files archived")
    stepper.complete(4)

    # Final status
    console.print("\n")
    console.print(stepper)

    console.print("\n")
    if processor.failed_files:
        console.print(
            Alert.warning(
                "Processing completed with warnings",
                details=f"{len(processor.failed_files)} files failed to process",
            )
        )
    else:
        console.print(
            Alert.success(
                "All files processed successfully",
                details=f"Processed {len(processor.processed_files)} files",
            )
        )

    # Next steps
    console.print("\n")
    with Section("Next Steps") as section:
        section.add_text("✓ Processed files available in /data/processed/", style="green")
        section.add_text("✓ Original files archived to /data/archive/", style="green")
        section.add_text(
            "✓ Full report saved to /data/reports/batch_20240101_143022.json", style="green"
        )

        if processor.failed_files:
            section.add_spacing()
            section.add_text(
                "⚠ Review failed files in /data/failed/ for manual processing", style="yellow"
            )


if __name__ == "__main__":
    run_file_processor()
