import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { Target, Loader2 } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

const PriorityScoring = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  const [formData, setFormData] = useState({
    domain: "Health",
    district: "Mumbai",
    issue_type: "Hospital_Bed_ICU",
    requests: 120,
    complaints: 15,
    response_time: 48.0,
    is_monsoon: 0,
    population_factor: 2.5,
    resolution_rate: 0.5,
    severity_level: "Critical",
  });

  const districts = ["Mumbai", "Pune", "Nagpur", "Thane", "Kolhapur", "Nashik"];
  const domains = ["Health", "Infrastructure", "PublicSafety"];
  const severityLevels = ["Critical", "High", "Medium", "Low"];
  const issueTypes = {
    Health: ["Hospital_Bed_ICU", "Hospital_Bed_General", "Ambulance_Emergency", "OPD_General", "OPD_Pediatric"],
    Infrastructure: ["Water_Supply_Shortage", "Electricity_Outage", "Road_Pothole_Repair", "Drainage_Block"],
    PublicSafety: ["Fire_Emergency", "Crime_High", "Accident_Spot", "Disaster_Alert"],
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch("https://api.predictivminds.shop/api/v1/predict/priority", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data);
        toast.success("Priority score calculated!");
      } else {
        toast.error("Failed to calculate priority");
      }
    } catch (error) {
      toast.error("Error connecting to backend. Using demo data.");
      setResult({
        priority_score: 8.7,
        priority_level: "HIGH",
        components: {
          urgency: 9.2,
          impact: 8.5,
          resources: 7.8,
          sentiment: 8.9,
        },
        recommendation: "Deploy emergency response team within 2 hours. Allocate additional resources from central reserve. Notify district coordinator for immediate action.",
      });
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (level: string) => {
    switch (level?.toLowerCase()) {
      case "critical": return "destructive";
      case "high": return "secondary";
      case "medium": return "default";
      case "low": return "outline";
      default: return "outline";
    }
  };

  const getPriorityGradient = (score: number) => {
    if (score >= 8) return "from-destructive to-destructive/70";
    if (score >= 6) return "from-secondary to-secondary/70";
    if (score >= 4) return "from-primary to-primary/70";
    return "from-health to-health/70";
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground mb-2">Priority Scoring</h1>
        <p className="text-muted-foreground">
          Calculate priority scores to optimize resource allocation and response strategies
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <Card>
          <CardHeader>
            <CardTitle>Issue Parameters</CardTitle>
            <CardDescription>Configure priority scoring variables</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label>Domain</Label>
                <Select
                  value={formData.domain}
                  onValueChange={(value) => setFormData({ ...formData, domain: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {domains.map((d) => (
                      <SelectItem key={d} value={d}>{d}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

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
                <Label>Issue Type</Label>
                <Select
                  value={formData.issue_type}
                  onValueChange={(value) => setFormData({ ...formData, issue_type: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {issueTypes[formData.domain as keyof typeof issueTypes]?.map((type) => (
                      <SelectItem key={type} value={type}>{type.replace(/_/g, " ")}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Requests</Label>
                  <Input
                    type="number"
                    value={formData.requests}
                    onChange={(e) => setFormData({ ...formData, requests: parseInt(e.target.value) })}
                  />
                </div>

                <div className="space-y-2">
                  <Label>Complaints</Label>
                  <Input
                    type="number"
                    value={formData.complaints}
                    onChange={(e) => setFormData({ ...formData, complaints: parseInt(e.target.value) })}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label>Response Time (hours)</Label>
                <Input
                  type="number"
                  step="0.5"
                  value={formData.response_time}
                  onChange={(e) => setFormData({ ...formData, response_time: parseFloat(e.target.value) })}
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
                <Label>Resolution Rate: {(formData.resolution_rate * 100).toFixed(0)}%</Label>
                <Slider
                  value={[formData.resolution_rate]}
                  onValueChange={([value]) => setFormData({ ...formData, resolution_rate: value })}
                  min={0}
                  max={1}
                  step={0.05}
                />
              </div>

              <div className="space-y-2">
                <Label>Severity Level</Label>
                <Select
                  value={formData.severity_level}
                  onValueChange={(value) => setFormData({ ...formData, severity_level: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {severityLevels.map((s) => (
                      <SelectItem key={s} value={s}>{s}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <Button
                type="button"
                variant="outline"
                className="w-full"
                onClick={() => {
                  setFormData({
                    domain: "Health",
                    district: "Mumbai",
                    issue_type: "Hospital_Bed_ICU",
                    requests: 120,
                    complaints: 15,
                    response_time: 48.0,
                    is_monsoon: 0,
                    population_factor: 2.5,
                    resolution_rate: 0.5,
                    severity_level: "Critical",
                  });
                  toast.info("Loaded example: Health Critical");
                }}
              >
                Load Example
              </Button>

              <Button type="submit" disabled={loading} className="w-full">
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Calculating...
                  </>
                ) : (
                  <>
                    <Target className="mr-2 h-4 w-4" />
                    Calculate Priority
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
              <Card className="overflow-hidden">
                <div className={cn(
                  "h-2 bg-gradient-to-r",
                  getPriorityGradient(result.priority_score || 0)
                )} />
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Target className="h-5 w-5 text-primary" />
                    Priority Assessment
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  {/* Main Priority Score Display */}
                  <div className="text-center p-8 bg-muted/50 rounded-lg">
                    <p className="text-sm text-muted-foreground mb-2">Priority Score</p>
                    <div className="flex items-center justify-center gap-4">
                      <p className={cn(
                        "text-7xl font-bold",
                        (result.priority_score || 0) >= 8 && "text-destructive",
                        (result.priority_score || 0) >= 6 && (result.priority_score || 0) < 8 && "text-secondary",
                        (result.priority_score || 0) >= 4 && (result.priority_score || 0) < 6 && "text-primary",
                        (result.priority_score || 0) < 4 && "text-health"
                      )}>
                        {(result.priority_score || 0).toFixed(1)}
                      </p>
                      <div className="text-left">
                        <Badge variant={getPriorityColor(result.priority_level)} className="mb-2">
                          {result.priority_level}
                        </Badge>
                        <p className="text-xs text-muted-foreground">out of 10.0</p>
                      </div>
                    </div>
                  </div>

                  {/* Overall Priority Bar */}
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-muted-foreground">Priority Level</span>
                      <span className="font-semibold">{result.priority_level}</span>
                    </div>
                    <div className="w-full bg-muted rounded-full h-3 overflow-hidden">
                      <div
                        className={cn(
                          "h-full transition-all duration-500 bg-gradient-to-r",
                          getPriorityGradient(result.priority_score || 0)
                        )}
                        style={{ width: `${((result.priority_score || 0) / 10) * 100}%` }}
                      />
                    </div>
                  </div>

                  {/* Components Breakdown */}
                  {result.components && (
                    <div className="space-y-4 pt-4 border-t">
                      <p className="text-sm font-semibold text-muted-foreground">Priority Components</p>
                      
                      {/* Urgency */}
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-muted-foreground">Urgency</span>
                          <span className="font-semibold">{result.components.urgency?.toFixed(1) || '0.0'} / 10</span>
                        </div>
                        <div className="w-full bg-muted rounded-full h-2.5 overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-red-500 to-red-600 transition-all duration-500"
                            style={{ width: `${((result.components.urgency || 0) / 10) * 100}%` }}
                          />
                        </div>
                      </div>

                      {/* Impact */}
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-muted-foreground">Impact</span>
                          <span className="font-semibold">{result.components.impact?.toFixed(1) || '0.0'} / 10</span>
                        </div>
                        <div className="w-full bg-muted rounded-full h-2.5 overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-orange-500 to-orange-600 transition-all duration-500"
                            style={{ width: `${((result.components.impact || 0) / 10) * 100}%` }}
                          />
                        </div>
                      </div>

                      {/* Resources */}
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-muted-foreground">Resources</span>
                          <span className="font-semibold">{result.components.resources?.toFixed(1) || '0.0'} / 10</span>
                        </div>
                        <div className="w-full bg-muted rounded-full h-2.5 overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-blue-500 to-blue-600 transition-all duration-500"
                            style={{ width: `${((result.components.resources || 0) / 10) * 100}%` }}
                          />
                        </div>
                      </div>

                      {/* Sentiment */}
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-muted-foreground">Sentiment</span>
                          <span className="font-semibold">{result.components.sentiment?.toFixed(1) || '0.0'} / 10</span>
                        </div>
                        <div className="w-full bg-muted rounded-full h-2.5 overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-purple-500 to-purple-600 transition-all duration-500"
                            style={{ width: `${((result.components.sentiment || 0) / 10) * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Recommendation */}
              {result.recommendation && (
                <Card className="border-l-4 border-l-primary">
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <Target className="h-5 w-5" />
                      Recommended Action
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
                <Target className="h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground text-center">
                  Configure issue parameters and calculate priority to view results
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default PriorityScoring;
