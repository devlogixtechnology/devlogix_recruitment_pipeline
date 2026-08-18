# Devlogix Recruitment Pipeline

## Overview

This project implements an automated email ingestion layer for the DevLogix recruitment pipeline.

The system connects to the DevLogix recruitment Gmail account through secure IMAP, identifies recruitment-related emails, extracts candidate CV attachments, saves them locally, optionally uploads them to Google Drive, and sends a notification when new CVs are processed.

The system is designed so that company credentials and deployment-specific configuration are provided by the DevLogix administrator and are not included in the source code.

---

## Features

- Secure Gmail IMAP connection using SSL/TLS
- Retrieval of recruitment emails
- Email date filtering
- Recruitment subject filtering
- Duplicate email detection using Message-ID
- PDF and DOCX attachment detection
- Unsafe filename sanitization
- Automatic local CV storage
- Duplicate filename protection
- Optional Google Drive upload
- Optional webhook notifications
- Environment-variable based configuration
- Credential protection through `.gitignore`
- Local testing without requiring company credentials

---

## System Workflow

```text
DevLogix Recruitment Gmail
          |
          v
      IMAP / SSL
          |
          v
     Email Retrieval
          |
          v
       Date Filter
          |
          v
   Recruitment Filter
          |
          v
   Duplicate Detection
          |
          v
 Attachment Validation
      /          \
   PDF/DOCX      Other
      |            |
      v            v
   Process       Ignore
      |
      v
 Local Storage
      |
      v
 Google Drive
 (if configured)
      |
      v
 Notification
 (if configured)
      |
      v
 Mark Email Processed
