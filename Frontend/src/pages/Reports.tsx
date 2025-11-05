import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { BarChart3, TrendingUp, Download, Calendar, MapPin, Activity } from "lucide-react";
import { toast } from "sonner";

const Reports = () => {
  const [dateRange, setDateRange] = useState("30");
  const [district, setDistrict] = useState("all");

  const handleExportPDF = () => {
    toast.success("Generating PDF report...");
    // Implement PDF export logic
  };

  const handleExportExcel = () => {
    toast.success("Generating Excel report...");
    // Implement Excel export logic
  };

  // Demo data
  const stats = {
    predictions_made: 1247,
    crises_prevented: 8,
    accuracy_rate: 92,
    districts_active: 36,
  };

  const districtData = [
    { district: "Mumbai", predictions: 342, crises: 3, accuracy: 94 },
    { district: "Pune", predictions: 256, crises: 2, accuracy: 91 },
    { district: "Nagpur", predictions: 189, crises: 1, accuracy: 90 },
    { district: "Thane", predictions: 178, crises: 1, accuracy: 93 },
    { district: "Nashik", predictions: 145, crises: 1, accuracy: 89 },
    { district: "Others", predictions: 137, crises: 0, accuracy: 92 },
  ];

  const crisisTypes = [
    { type: "Water Shortage", count: 3, severity: "HIGH" },
    { type: "Hospital Capacity", count: 2, severity: "CRITICAL" },
    { type: "Road Infrastructure", count: 2, severity: "MEDIUM" },
    { type: "Power Outage", count: 1, severity: "MEDIUM" },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground mb-2">
          📊 REPORTS & ANALYTICS
        </h1>
        <p className="text-muted-foreground">
          Historical trends and patterns analysis
        </p>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Filters</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-4">
          <div className="flex items-center gap-2">
            <Calendar className="h-4 w-4 text-muted-foreground" />
            <Select value={dateRange} onValueChange={setDateRange}>
              <SelectTrigger className="w-[180px]">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="7">Last 7 Days</SelectItem>
                <SelectItem value="30">Last 30 Days</SelectItem>
                <SelectItem value="90">Last 90 Days</SelectItem>
                <SelectItem value="365">Last Year</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="flex items-center gap-2">
            <MapPin className="h-4 w-4 text-muted-foreground" />
            <Select value={district} onValueChange={setDistrict}>
              <SelectTrigger className="w-[180px]">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Districts</SelectItem>
                <SelectItem value="Mumbai">Mumbai</SelectItem>
                <SelectItem value="Pune">Pune</SelectItem>
                <SelectItem value="Nagpur">Nagpur</SelectItem>
                <SelectItem value="Thane">Thane</SelectItem>
                <SelectItem value="Nashik">Nashik</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="ml-auto flex gap-2">
            <Button variant="outline" onClick={handleExportExcel}>
              <Download className="mr-2 h-4 w-4" />
              Export Excel
            </Button>
            <Button onClick={handleExportPDF}>
              <Download className="mr-2 h-4 w-4" />
              Export PDF
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="border-l-4 border-l-primary">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Predictions Made
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <p className="text-3xl font-bold">{stats.predictions_made}</p>
              <Activity className="h-8 w-8 text-primary opacity-50" />
            </div>
            <p className="text-xs text-muted-foreground mt-2">
              In last {dateRange} days
            </p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-green-500">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Crises Prevented
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <p className="text-3xl font-bold">{stats.crises_prevented}</p>
              <TrendingUp className="h-8 w-8 text-green-500 opacity-50" />
            </div>
            <p className="text-xs text-green-600 dark:text-green-400 mt-2">
              Early intervention successful
            </p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-blue-500">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Accuracy Rate
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <p className="text-3xl font-bold">{stats.accuracy_rate}%</p>
              <BarChart3 className="h-8 w-8 text-blue-500 opacity-50" />
            </div>
            <p className="text-xs text-muted-foreground mt-2">
              Model performance
            </p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-purple-500">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Districts Active
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <p className="text-3xl font-bold">{stats.districts_active}</p>
              <MapPin className="h-8 w-8 text-purple-500 opacity-50" />
            </div>
            <p className="text-xs text-muted-foreground mt-2">
              Across Maharashtra
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: Predictions by District */}
        <Card>
          <CardHeader>
            <CardTitle>📊 Predictions by District</CardTitle>
            <CardDescription>Total predictions made per district</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {districtData.map((item) => (
                <div key={item.district}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium">{item.district}</span>
                    <span className="text-sm text-muted-foreground">{item.predictions}</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-2">
                    <div
                      className="bg-primary h-2 rounded-full"
                      style={{ width: `${(item.predictions / 342) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Chart 2: Crisis Types Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>🚨 Crisis Types Distribution</CardTitle>
            <CardDescription>Breakdown of detected crises</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {crisisTypes.map((item) => (
                <div key={item.type} className="flex items-center justify-between">
                  <div className="flex items-center gap-3 flex-1">
                    <div
                      className={`w-3 h-3 rounded-full ${
                        item.severity === "CRITICAL"
                          ? "bg-destructive"
                          : item.severity === "HIGH"
                          ? "bg-orange-500"
                          : "bg-yellow-500"
                      }`}
                    />
                    <span className="text-sm font-medium">{item.type}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">{item.count} cases</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Chart 3: Priority Trends Over Time */}
      <Card>
        <CardHeader>
          <CardTitle>📈 Priority Trends Over Time</CardTitle>
          <CardDescription>How priorities changed over the selected period</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-64 flex items-center justify-center bg-muted/20 rounded-lg border-2 border-dashed">
            <div className="text-center">
              <TrendingUp className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
              <p className="text-muted-foreground">
                Time series visualization
              </p>
              <p className="text-sm text-muted-foreground mt-2">
                Shows CRITICAL, HIGH, MEDIUM, LOW trends over {dateRange} days
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Summary Section */}
      <Card className="bg-primary/5 border-primary">
        <CardHeader>
          <CardTitle>📋 Summary</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <p>
            ✅ In the last {dateRange} days, the system made{" "}
            <strong>{stats.predictions_made} predictions</strong> across{" "}
            <strong>{stats.districts_active} districts</strong>.
          </p>
          <p>
            ✅ <strong>{stats.crises_prevented} crises were prevented</strong> through early
            intervention and proactive resource allocation.
          </p>
          <p>
            ✅ The AI models achieved an accuracy rate of{" "}
            <strong>{stats.accuracy_rate}%</strong>, demonstrating reliable
            performance.
          </p>
          <p>
            ✅ <strong>Mumbai</strong> had the highest prediction activity with{" "}
            <strong>{districtData[0].predictions} predictions</strong> and{" "}
            <strong>{districtData[0].crises} crises detected</strong>.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default Reports;
