The code’s weight parameters are derived from the model. To make it easier for non-AI specialists to understand the code and to reduce runtime, this version only retains the model’s results and removes the model architecture.
Grading System (modifiable)
Each indicator is first mapped to a score from 0–3 (0 = green/best, 3 = dark red/worst). A weighted average is then calculated to obtain a total score (0–3), which is finally mapped into four grades:
* 0–0.75: Green
* 0.75–1.5: Yellow
* 1.5–2.25: Orange
* >2.25: Dark Red
Indicator Scoring Rules
* DO_mg: ≥8 (0), 6–8 (1), 4–6 (2), <4 (3)
* TSS (mg/L): <5 (0), 5–20 (1), 20–50 (2), >50 (3)
* Sal (typical bay range): 30–38 (0), 25–30 or 38–41 (1), 20–25 or 41–44 (2), others (3)
Nutrients (N_TOTAL, P_PO4, P_TOTAL) are originally in mg/L. For threshold comparison, they are multiplied by 1000 to convert to µg/L, then compared with Australian water quality standards (µg/L):
* N_Total (µg/L, after mg/L × 1000): <150 (0), 150–300 (1), 300–600 (2), >600 (3)
* P_PO4 (µg/L): <30 (0), 30–60 (1), 60–120 (2), >120 (3)
* P_Total (µg/L): <45 (0), 45–90 (1), 90–180 (2), >180 (3)
Default Weights (from model)
* DO: 0.25
* TSS: 0.20
* Sal: 0.05
* N_Total: 0.20
* P_PO4: 0.15
* P_Total: 0.15
If a value is missing, weights for the non-missing indicators are renormalized. Each available indicator’s score is multiplied by its weight, summed, and divided only by the sum of the available weights.


*Most Recent Year per Monitoring Site*
For each site, the latest date in the dataset is identified. A 365-day window prior to that date is then used as the “most recent year” for that site. The mean value within this window is calculated, ensuring consistency even when sites have different data coverage periods.

