import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Slider } from "@/components/ui/slider";
import { AlertTriangle, Loader2 } from "lucide-react";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

const CrisisPrediction = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  const [formData, setFormData] = useState({
    district: "Mumbai",
    month: 4,
    is_monsoon: 0,
    population_factor: 2.5,
    demand_requests: 150,
    pending_requests: 90,
    citizen_complaints: 18,
    response_time_hours: 72.0,
    demand_lag_7days: 140.0,
    demand_lag_30days: 100.0,
    resolution_rate: 0.3,
  });

  const districts = ["Mumbai", "Pune", "Nagpur", "Thane", "Kolhapur", "Nashik"];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch("https://api.predictivminds.shop/api/v1/predict/crisis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data);
        toast.success("Crisis assessment completed!");
      } else {
        toast.error("Failed to assess crisis risk");
      }
    } catch (error) {
      toast.error("Error connecting to backend. Using demo data.");
      setResult({
        crisis_detected: true,
        probability: 0.78,
        risk_level: "HIGH",
        days_until_crisis: 5,
        affected_population: 50000,
        recommendation: "Increase emergency response teams by 25%. Activate standby resources in neighboring districts. Implement 24/7 monitoring protocol.",
      });
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level: string) => {
    switch (level?.toLowerCase()) {
      case "critical": return "destructive";
      case "high": return "secondary";
      case "medium": return "default";
      case "low": return "health";
      default: return "muted";
    }
  };

  const getRiskBgClass = (level: string) => {
    switch (level?.toLowerCase()) {
      case "critical": return "bg-destructive/10 border-destructive";
      case "high": return "bg-secondary/10 border-secondary";
      case "medium": return "bg-primary/10 border-primary";
      case "low": return "bg-health/10 border-health";
      default: return "bg-muted";
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground mb-2">Crisis Prediction</h1>
        <p className="text-muted-foreground">
          Assess and predict potential crisis situations requiring immediate intervention
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <Card>
          <CardHeader>
            <CardTitle>Assessment Parameters</CardTitle>
            <CardDescription>Configure crisis prediction variables</CardDescription>
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
                <Label>Month (1-12)</Label>
                <Input
                  type="number"
                  min="1"
                  max="12"
                  value={formData.month}
                  onChange={(e) => setFormData({ ...formData, month: parseInt(e.target.value) })}
                />
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
                <Label>Demand Requests</Label>
                <Input
                  type="number"
                  value={formData.demand_requests}
                  onChange={(e) => setFormData({ ...formData, demand_requests: parseInt(e.target.value) })}
                />
              </div>

              <div className="space-y-2">
                <Label>Pending Requests</Label>
                <Input
                  type="number"
                  value={formData.pending_requests}
                  onChange={(e) => setFormData({ ...formData, pending_requests: parseInt(e.target.value) })}
                />
              </div>

              <div className="space-y-2">
                <Label>Citizen Complaints</Label>
                <Input
                  type="number"
                  value={formData.citizen_complaints}
                  onChange={(e) => setFormData({ ...formData, citizen_complaints: parseInt(e.target.value) })}
                />
              </div>

              <div className="space-y-2">
                <Label>Response Time (hours)</Label>
                <Input
                  type="number"
                  step="0.5"
                  value={formData.response_time_hours}
                  onChange={(e) => setFormData({ ...formData, response_time_hours: parseFloat(e.target.value) })}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Demand Lag 7 Days</Label>
                  <Input
                    type="number"
                    step="0.1"
                    value={formData.demand_lag_7days}
                    onChange={(e) => setFormData({ ...formData, demand_lag_7days: parseFloat(e.target.value) })}
                  />
                </div>
                <div className="space-y-2">
                  <Label>Demand Lag 30 Days</Label>
                  <Input
                    type="number"
                    step="0.1"
                    value={formData.demand_lag_30days}
                    onChange={(e) => setFormData({ ...formData, demand_lag_30days: parseFloat(e.target.value) })}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label>Resolution Rate: {(formData.resolution_rate * 100).toFixed(0)}%</Label>
                <Slider
                  value={[formData.resolution_rate]}
                  onValueChange={([value]) => setFormData({ ...formData, resolution_rate: value })}
                  min={0}
                  max={1}
                  step={0.05}
                />
              </div>

              <Button
                type="button"
                variant="outline"
                className="w-full"
                onClick={() => {
                  setFormData({
                    district: "Mumbai",
                    month: 4,
                    is_monsoon: 0,
                    population_factor: 2.5,
                    demand_requests: 150,
                    pending_requests: 90,
                    citizen_complaints: 18,
                    response_time_hours: 72.0,
                    demand_lag_7days: 140.0,
                    demand_lag_30days: 100.0,
                    resolution_rate: 0.3,
                  });
                  toast.info("Loaded example: CRITICAL High Risk");
                }}
              >
                Load Example
              </Button>              <Button type="submit" disabled={loading} className="w-full">
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Assessing...
                  </>
                ) : (
                  <>
                    <AlertTriangle className="mr-2 h-4 w-4" />
                    Assess Crisis Risk
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Results Display */}
        <div className="space-y-6">
          {result && (
            <>
              <Card className={cn("border-2", getRiskBgClass(result.risk_level))}>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <AlertTriangle className="h-5 w-5" />
                    Crisis Risk Assessment
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  {/* Crisis Alert Banner */}
                  {result.crisis_detected && (
                    <div className="bg-destructive/10 border-2 border-destructive rounded-lg p-6 text-center">
                      <div className="flex items-center justify-center gap-2 mb-2">
                        <AlertTriangle className="h-8 w-8 text-destructive" />
                        <p className="text-2xl font-bold text-destructive">🚨 CRISIS ALERT</p>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        Immediate action required to prevent crisis escalation
                      </p>
                    </div>
                  )}

                  {/* Main Risk Level Display */}
                  <div className={cn("p-8 rounded-lg border-2 text-center", getRiskBgClass(result.risk_level))}>
                    <p className="text-sm text-muted-foreground mb-2">Risk Level</p>
                    <p className="text-6xl font-bold mb-4" style={{ 
                      color: `hsl(var(--${getRiskColor(result.risk_level)}))` 
                    }}>
                      {result.risk_level}
                    </p>
                    <p className="text-lg text-muted-foreground">
                      Probability: {((result.probability || 0) * 100).toFixed(0)}%
                    </p>
                  </div>

                  {/* Probability Bar */}
                  <div className="w-full bg-muted rounded-full h-3 overflow-hidden">
                    <div
                      className={cn("h-full transition-all duration-500")}
                      style={{
                        width: `${(result.probability || 0) * 100}%`,
                        backgroundColor: `hsl(var(--${getRiskColor(result.risk_level)}))`,
                      }}
                    />
                  </div>

                  {/* Crisis Details Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Days Until Crisis */}
                    <Card className="border-orange-200 bg-orange-50 dark:bg-orange-950/20">
                      <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground mb-2">Time Until Crisis</p>
                        <p className="text-4xl font-bold text-orange-600 dark:text-orange-400">
                          {result.days_until_crisis || 0}
                        </p>
                        <p className="text-sm text-muted-foreground mt-1">days</p>
                      </CardContent>
                    </Card>

                    {/* Affected Population */}
                    <Card className="border-red-200 bg-red-50 dark:bg-red-950/20">
                      <CardContent className="p-6">
                        <p className="text-sm text-muted-foreground mb-2">Affected Population</p>
                        <p className="text-4xl font-bold text-red-600 dark:text-red-400">
                          {result.affected_population?.toLocaleString() || '0'}
                        </p>
                        <p className="text-sm text-muted-foreground mt-1">people at risk</p>
                      </CardContent>
                    </Card>
                  </div>
                </CardContent>
              </Card>

              {/* Recommendations */}
              {result.recommendation && (
                <Card className="border-l-4 border-l-primary">
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <AlertTriangle className="h-5 w-5" />
                      Urgent Recommendation
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-foreground leading-relaxed">
                      {result.recommendation}
                    </p>
                  </CardContent>
                </Card>
              )}
            </>
          )}

          {!result && (
            <Card className="border-dashed">
              <CardContent className="flex flex-col items-center justify-center py-16">
                <AlertTriangle className="h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground text-center">
                  Configure parameters and assess crisis risk to view results
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default CrisisPrediction;
