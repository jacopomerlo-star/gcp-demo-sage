# Bucket dei documenti sorgente di Sage. Gestito da Terraform: il suffisso "-sage-docs"
# lo distingue dai bucket creati a mano negli esercizi CLI/Console del corso, che usano
# "-manual-docs" per non entrare mai in conflitto con questa risorsa.
resource "google_storage_bucket" "sage_docs" {
  name          = "${local.name_prefix}-${var.docs_bucket_suffix}"
  project       = var.project_id
  location      = var.region
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
  force_destroy               = true # comodo in un progetto didattico usa-e-getta

  depends_on = [google_project_service.apis]
}

# Bucket delle istruzioni di sistema per Sage (<prefisso>-instructions).
resource "google_storage_bucket" "sage_instructions" {
  name          = "${local.name_prefix}-instructions"
  project       = var.project_id
  location      = var.region
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
  force_destroy               = true

  depends_on = [google_project_service.apis]
}

# Permesso di lettura al service account di Cloud Run sul bucket delle istruzioni.
resource "google_storage_bucket_iam_member" "sage_run_instructions_viewer" {
  bucket = google_storage_bucket.sage_instructions.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.sage_run.email}"
} 