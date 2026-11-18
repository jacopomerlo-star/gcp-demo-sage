variable "project_id" {
  description = "ID del progetto GCP"
  type        = string
}

variable "region" {
  description = "Regione GCP in cui creare le risorse"
  type        = string
}

variable "resource_prefix" {
  description = "Prefisso usato per i nomi delle risorse"
  type        = string
}
variable "docs_bucket_suffix" {
  description = "Suffisso del bucket dei documenti sorgente"
  type        = string
  default     = "sage-docs"
}

variable "firestore_collection" {
  description = "Nome della collection Firestore per i chunk indicizzati"
  type        = string
  default     = "chunks"
}

variable "embedding_dimension" {
  description = "Dimensione del vettore di embedding"
  type        = number
  default     = 768
}

variable "bq_table" {
  description = "Nome della tabella BigQuery per il log delle domande"
  type        = string
  default     = "question_log"
} 