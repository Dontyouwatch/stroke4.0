<script>
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Show loading state
    document.getElementById('loadingIndicator').style.display = 'block';
    document.getElementById('result-container').style.display = 'none';

    try {
      // Get all form values
      const formData = {
        age: parseFloat(document.getElementById('age').value),
        sex: document.getElementById('sex').value,
        bmi: parseFloat(document.getElementById('bmi').value),
        cholesterol: parseFloat(document.getElementById('cholesterol').value),
        hypertension: parseInt(document.getElementById('hypertension').value),
        atrial_fibrillation: parseInt(document.getElementById('atrial-fibrillation').value),
        diabetes: parseInt(document.getElementById('diabetes').value),
        smoking: parseInt(document.getElementById('smoking').value),
        previous_stroke: parseInt(document.getElementById('previous-stroke').value)
      };

      // 1. First calculate risk using medical algorithm
      const medicalRiskPercentage = calculateMedicalRisk(formData);
      
      // 2. Then calculate risk using ML model via API call
      const mlResponse = await fetch('/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });
      
      if (!mlResponse.ok) {
        throw new Error('Failed to get ML prediction');
      }
      
      const mlData = await mlResponse.json();
      const mlRiskPercentage = mlData.risk_percentage;
      
      // 3. Combine both results (weighted average)
      const combinedRiskPercentage = combineRisks(medicalRiskPercentage, mlRiskPercentage);
      
      // Prepare result object
      const result = {
        medical_risk: medicalRiskPercentage,
        ml_risk: mlRiskPercentage,
        combined_risk: combinedRiskPercentage,
        formData: formData
      };

      displayResults(result);
      
    } catch (error) {
      console.error('Error:', error);
      showError(error.message || 'Failed to get prediction. Please try again.');
    } finally {
      document.getElementById('loadingIndicator').style.display = 'none';
    }
  });
