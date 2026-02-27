# Hardware

- Cameras (could be many, must be synchronous)
- Image Storage (Google Cloud Storage)
- Result Storage (text only, could be Postgre)
- GPU to run pytorch transformer model
---

# Requirements

Business:

- Takes inputs from cameras, then produce information written on box if seen one

Architecture:

- We should able to store images as training data
- Result should be also stored for error analysis
- Model for both box detection and box reader should be easy to train/ fine tune (data from image storage and result storage)
- Model hould be swappable for faster inference engine when inference
- Inference time should be less than 10 seconds to produce box information and accuracy of 100%
- The whole system run 24/24 with no downtimes
- Changing from training to inferencing should not requires changing any bussiness/ domain code

---

# General Pipeline

Takes inputs from cameras, then to box detection model, if no, discard, if yes, given the same raw frame:

- Store image to image storage
- Call model box reader to produce result

Model box reader then add its result to result storage (for analysis).

---

# Architecture

## `src\config`

### Responsibility

Centralized, declarative configuration of the system.

### What lives here:

- Environment-based settings
- Model configuration (paths, versions, thresholds)
- Storage configuration (GCS buckets, DB connection)
- Runtime mode (training vs inference)

### Characteristics:

- Uses pydantic-settings
- No business logic
- No imports from services, computer_vision, or infrastructure

---

## `src\domain`

### Responsibility

Defines what the system is, not how it works.

### What lives here

Entities:
- Image
- BoxInformation
- Result

Interfaces / ports:
- ImageStream
- BoxDetector
- BoxReader
- ImageRepository
- ResultRepository

### Characteristics
- Pure Python
- No OpenCV, no PyTorch, no cloud SDKs
- No side effects
- Fully testable without mocks

---

## `src\computer_vision`

### Responsibility

Concrete ML / CV implementations. Just like a second infrastructure

### What lives here

- PyTorch / Transformers models
- HF-based implementations
- TensorRT / ONNX / OpenVINO versions
- Dummys inputs from video for testing
- Pre/post-processing logic

### Examples

- HFBoxDetector
- HFBoxReader
- ONNXBoxDetector
- TensorRTBoxReader

### Characteristics

- Implements domain interfaces
- Heavy dependencies allowed
- Multiple implementations per interface

### Why

- Models are swappable
- Training and inference share the same contracts
- Optimized engines can replace research models without touching domain code

---

## `src\infrastructure`

### Responsibility
External systems, IO, and side effects.

### What lives here
- Camera implementations (OpenCV, RTSP)
- Image storage (Google Cloud Storage)
- Result storage (PostgreSQL)
- File system, network, serialization

### Examples
- CVCameraStream
- GCSImageRepository
- PostgresResultRepository

### Characteristics
- Implements domain ports
- Talks to the outside world
- Replaceable without changing services

### Why
- Enables offline testing
- Allows future migration (e.g. S3 instead of GCS)
- Keeps failures contained

---

## `src\services`

### Responsibility
Application orchestration and business workflows.

### What lives here
- Image reading coordination
- Detection → storage → reading pipeline
- Error handling and retries
- Throughput and latency management

### Examples
- ImageReaderService
- BoxDetectService
- BoxReadService
- PipelineService

### Characteristics
- Depends on domain interfaces
- No knowledge of concrete implementations
- Stateless or minimally stateful

### Why
- Business rules live here
- Easy to test with fake adapters
- Stable over time even as tech evolves

## `src\controller`

### Responsibility
Application entrypoints and composition root.

### What lives here
- Wiring of concrete implementations
- Startup / shutdown logic
- Runtime mode selection
- CLI / API / worker processes

### Examples
- box_detection.py
- training_pipeline.py
- replay_from_storage.py

### Characteristics
- Knows everything
- Changes often
- Not reusable

### Why
- Keeps complexity out of services
- Enables multiple runtimes from same codebase
- Supports zero-downtime deploys