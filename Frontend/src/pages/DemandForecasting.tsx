import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Slider } from "@/components/ui/slider";
import { TrendingUp, Loader2 } from "lucide-react";
import { toast } from "sonner";

const DemandForecasting = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  const [formData, setFormData] = useState({
    district: "Mumbai",
    service_type: "Ambulance_Emergency",
    month: 7,
    day_of_week: 1,
    is_weekend: 0,
    is_monsoon: 1,
    population_factor: 2.5,
    urban_ratio: 1.0,
    demand_lag_7days: 45.0,
    demand_lag_30days: 42.0,
    resource_utilization_rate: 0.75,
    complaint_rate: 0.15,
    response_time_minutes: 16.5,
  });

  const districts = ["Mumbai", "Pune", "Nagpur", "Thane", "Kolhapur", "Nashik"];
  const serviceTypes = [
    "Ambulance_Emergency",
    "Hospital_Bed_General",
    "Hospital_Bed_ICU",
    "OPD_Pediatric",
    "OPD_General",
    "Disease_Dengue",
    "Disease_Malaria",
    "Water_Supply",
    "Electricity_Outage",
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch("https://api.predictivminds.shop/api/v1/predict/demand", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("API Response:", data); // Debug log
        
        // Extract prediction from response structure
        const predictionData = data.prediction || data;
        setResult(predictionData);
        toast.success("Demand forecast generated successfully!");
      } else {
        const errorData = await response.json();
        console.error("API Error:", errorData);
        toast.error(errorData.detail || "Failed to generate forecast");
      }
    } catch (error) {
      toast.error("Error connecting to backend. Using demo data.");
      setResult({
        predicted_demand: 245,
        confidence_score: 0.87,
        trend: "increasing",
        recommendation: "Allocate additional resources to meet forecasted demand",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground mb-2">Demand Forecasting</h1>
        <p className="text-muted-foreground">
          Predict service demand across health, infrastructure, and public safety domains
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <Card>
          <CardHeader>
            <CardTitle>Input Parameters</CardTitle>
            <CardDescription>Configure forecasting variables</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label>District</Label>
                <Select
                  value={formData.district}
                  onValueChange={(value) => setFormData({ ...formData, district: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {districts.map((d) => (
                      <SelectItem key={d} value={d}>{d}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Service Type</Label>
                <Select
                  value={formData.service_type}
                  onValueChange={(value) => setFormData({ ...formData, service_type: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {serviceTypes.map((s) => (
                      <SelectItem key={s} value={s}>{s.replace(/_/g, " ")}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Month (1-12)</Label>
                  <Input
                    type="number"
                    min="1"
                    max="12"
                    value={formData.month || ''}
                    onChange={(e) => setFormData({ ...formData, month: parseInt(e.target.value) || 1 })}
                  />
                </div>
                <div className="space-y-2">
                  <Label>Day of Week (0-6)</Label>
                  <Input
                    type="number"
                    min="0"
                    max="6"
                    value={formData.day_of_week || ''}
                    onChange={(e) => setFormData({ ...formData, day_of_week: parseInt(e.target.value) || 0 })}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label>Weekend</Label>
                <Select
                  value={formData.is_weekend.toString()}
                  onValueChange={(value) => setFormData({ ...formData, is_weekend: parseInt(value) })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="0">No</SelectItem>
                    <SelectItem value="1">Yes</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Monsoon Season</Label>
                <Select
                  value={formData.is_monsoon.toString()}
                  onValueChange={(value) => setFormData({ ...formData, is_monsoon: parseInt(value) })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="0">No</SelectItem>
                    <SelectItem value="1">Yes</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Population Factor: {formData.population_factor.toFixed(1)}</Label>
                <Slider
                  value={[formData.population_factor]}
                  onValueChange={([value]) => setFormData({ ...formData, population_factor: value })}
                  min={1.0}
                  max={2.5}
                  step={0.1}
                />
              </div>

              <div className="space-y-2">
                <Label>Urban Ratio: {formData.urban_ratio.toFixed(2)}</Label>
                <Slider
                  value={[formData.urban_ratio]}
                  onValueChange={([value]) => setFormData({ ...formData, urban_ratio: value })}
                  min={0}
                  max={1}
                  step={0.05}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Demand Lag 7 Days</Label>
                  <Input
                    type="number"
                    step="0.1"
                    value={formData.demand_lag_7days || ''}
                    onChange={(e) => setFormData({ ...formData, demand_lag_7days: parseFloat(e.target.value) || 0 })}
                  />
                </div>
                <div className="space-y-2">
                  <Label>Demand Lag 30 Days</Label>
                  <Input
                    type="number"
                    step="0.1"
                    value={formData.demand_lag_30days || ''}
                    onChange={(e) => setFormData({ ...formData, demand_lag_30days: parseFloat(e.target.value) || 0 })}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label>Resource Utilization Rate: {formData.resource_utilization_rate.toFixed(2)}</Label>
                <Slider
                  value={[formData.resource_utilization_rate]}
                  onValueChange={([value]) => setFormData({ ...formData, resource_utilization_rate: value })}
                  min={0}
                  max={1}
                  step={0.05}
                />
              </div>

              <div className="space-y-2">
                <Label>Complaint Rate: {formData.complaint_rate.toFixed(2)}</Label>
                <Slider
                  value={[formData.complaint_rate]}
                  onValueChange={([value]) => setFormData({ ...formData, complaint_rate: value })}
                  min={0}
                  max={0.5}
                  step={0.05}
                />
              </div>

              <div className="space-y-2">
                <Label>Response Time (minutes)</Label>
                <Input
                  type="number"
                  step="0.5"
                  value={formData.response_time_minutes || ''}
                  onChange={(e) => setFormData({ ...formData, response_time_minutes: parseFloat(e.target.value) || 0 })}
                />
              </div>

              <Button
                type="button"
                variant="outline"
                className="w-full"
                onClick={() => {
                  // Load example from Postman collection
                  setFormData({
                    district: "Mumbai",
                    service_type: "Ambulance_Emergency",
                    month: 7,
                    day_of_week: 1,
                    is_weekend: 0,
                    is_monsoon: 1,
                    population_factor: 2.5,
                    urban_ratio: 1.0,
                    demand_lag_7days: 45.0,
                    demand_lag_30days: 42.0,
                    resource_utilization_rate: 0.75,
                    complaint_rate: 0.15,
                    response_time_minutes: 16.5,
                  });
                  toast.info("Loaded example: High Demand Mumbai Monsoon");
                }}
              >
                Load Example
              </Button>

              <Button type="submit" disabled={loading} className="w-full">
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Forecasting...
                  </>
                ) : (
                  <>
                    <TrendingUp className="mr-2 h-4 w-4" />
                    Forecast Demand
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Results Display */}
        <div className="space-y-6">{result && (
            <>
              <Card className="border-primary">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-primary" />
                    Forecast Results
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-6 bg-primary/5 rounded-lg border border-primary">
                    <p className="text-sm text-muted-foreground mb-1">Predicted Demand</p>
                    <p className="text-5xl font-bold text-primary">
                      {typeof result.predicted_demand === 'number' 
                        ? result.predicted_demand.toFixed(1)
                        : result.predicted_demand || 'N/A'}
                    </p>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 bg-muted rounded-lg">
                      <p className="text-xs text-muted-foreground mb-1">Confidence Score</p>
                      <p className="text-2xl font-bold text-health">
                        {typeof result.confidence_score === 'number'
                          ? (result.confidence_score * 100).toFixed(0) + '%'
                          : result.confidence_score 
                          ? (parseFloat(result.confidence_score) * 100).toFixed(0) + '%'
                          : 'N/A'}
                      </p>
                    </div>
                    <div className="p-4 bg-muted rounded-lg">
                      <p className="text-xs text-muted-foreground mb-1">Trend</p>
                      <p className="text-2xl font-bold capitalize text-foreground">
                        {result.trend || 'N/A'}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {result.recommendation && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Recommendations</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">{result.recommendation}</p>
                  </CardContent>
                </Card>
              )}
            </>
          )}

          {!result && (
            <Card className="border-dashed">
              <CardContent className="flex flex-col items-center justify-center py-16">
                <TrendingUp className="h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground text-center">
                  Configure parameters and generate a forecast to view results
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default DemandForecasting;
