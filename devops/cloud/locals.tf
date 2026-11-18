locals {
  # Sostituisce eventuali punti con trattini per i nomi GCP (bucket, service account)
  name_prefix = replace(var.resource_prefix, ".", "-")

  app_name            = "${local.name_prefix}-${var.app_name}"
  sage_run_account_id = substr("${local.name_prefix}-run", 0, 30)

  # BigQuery accetta solo lettere, numeri e underscore (niente trattini)
  bq_dataset         = "${replace(local.name_prefix, "-", "_")}_analytics"
  firestore_database = "${local.name_prefix}-db"
} 