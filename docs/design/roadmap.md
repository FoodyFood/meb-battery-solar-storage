# Product Roadmap

From proof-of-concept to a commercially installable second-life MEB battery storage solution.

```mermaid
flowchart TD
    subgraph POC["Phase 1 — Proof of Concept"]
        P1["Simulator build\n(Arduino + MCP2518FD)"]
        P2["Battery-Emulator on ESP32\nfirst power-on"]
        P3["Contactor close achieved\nwith real battery"]
        P4["Digipot closed-loop\nprecharge validated"]
        P1 --> P2 --> P3 --> P4
    end

    subgraph PILOT["Phase 2 — Pilot System"]
        PI1["Inverter selected\nand integrated"]
        PI2["Charge / discharge\ncycle validated"]
        PI3["Safety testing\n(isolation, fault injection)"]
        PI4["Commissioning procedure\ndocumented"]
        PI1 --> PI2 --> PI3 --> PI4
    end

    subgraph INTEGRATION["Phase 3 — Integration"]
        I1["Custom PCB design\n(replaces dev boards)"]
        I2["Enclosure design\n(IP rating, HV safety)"]
        I3["Commissioning tool\n(web UI / app)"]
        I4["Battery health\nassessment procedure"]
        I1 --> I2
        I3 --> I4
    end

    subgraph PRODUCT["Phase 4 — Product"]
        PR1["Regulatory compliance\n(CE / electrical safety)"]
        PR2["Installation guide\nand documentation"]
        PR3["First customer\ninstallation"]
        PR4["Remote monitoring\n(fleet management)"]
        PR1 --> PR2 --> PR3 --> PR4
    end

    POC --> PILOT --> INTEGRATION --> PRODUCT

    classDef poc fill:#4ecdc4,stroke:#333,color:#fff
    classDef pilot fill:#5b7fff,stroke:#333,color:#fff
    classDef integration fill:#f39c12,stroke:#333,color:#fff
    classDef product fill:#9b59b6,stroke:#333,color:#fff

    class P1,P2,P3,P4 poc
    class PI1,PI2,PI3,PI4 pilot
    class I1,I2,I3,I4 integration
    class PR1,PR2,PR3,PR4 product
```

## Phase Summary

### Phase 1 — Proof of Concept
Validate the core technology: CAN FD communication, precharge sequence, and contactor control with a real MEB battery. All work done with dev boards and bench equipment.

### Phase 2 — Pilot System
Integrate an inverter and validate a full charge/discharge cycle. Develop safety testing procedures and a commissioning checklist. This phase produces the first working home storage system.

### Phase 3 — Integration
Replace dev boards with a custom PCB. Design an enclosure suitable for real-world installation. Build a commissioning tool for field use and a battery health assessment procedure for evaluating secondhand packs before purchase.

### Phase 4 — Product
Achieve regulatory compliance, produce installation documentation, and deliver the first customer installation. Add remote monitoring for fleet management as the install base grows.

## Current Status

We are in **Phase 1**, with hardware on order and the CAN FD protocol fully documented.
