import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import DemandForecasting from "./DemandForecasting";
import CrisisPrediction from "./CrisisPrediction";
import PriorityScoring from "./PriorityScoring";
import { Activity, AlertTriangle, ListOrdered } from "lucide-react";

const Predictions = () => {
  const [activeTab, setActiveTab] = useState("demand");

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground mb-2">
          🔮 PREDICTIONS
        </h1>
        <p className="text-muted-foreground">
          3 AI-powered models for governance decision making
        </p>
      </div>

      {/* Tabs for 3 Models */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-3 h-auto">
          <TabsTrigger value="demand" className="flex flex-col items-center gap-2 py-4">
            <Activity className="h-5 w-5" />
            <div className="text-left">
              <p className="font-semibold">Demand Forecasting</p>
              <p className="text-xs text-muted-foreground">
                Predict resource needs
              </p>
            </div>
          </TabsTrigger>
          <TabsTrigger value="crisis" className="flex flex-col items-center gap-2 py-4">
            <AlertTriangle className="h-5 w-5" />
            <div className="text-left">
              <p className="font-semibold">Crisis Detection</p>
              <p className="text-xs text-muted-foreground">
                Identify future risks
              </p>
            </div>
          </TabsTrigger>
          <TabsTrigger value="priority" className="flex flex-col items-center gap-2 py-4">
            <ListOrdered className="h-5 w-5" />
            <div className="text-left">
              <p className="font-semibold">Priority Scoring</p>
              <p className="text-xs text-muted-foreground">
                Rank issues urgency
              </p>
            </div>
          </TabsTrigger>
        </TabsList>

        {/* Tab 1: Demand Forecasting */}
        <TabsContent value="demand" className="space-y-4">
          <div className="bg-blue-50 dark:bg-blue-950 border-l-4 border-blue-500 p-4 rounded-lg">
            <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">
              💡 Use Case: "How many ambulances will Mumbai need tomorrow during monsoon?"
            </h3>
            <p className="text-sm text-blue-800 dark:text-blue-200">
              <strong>Example:</strong> Input Mumbai + July + Monsoon season + 45 calls last week
              → Output: Expect 58 ambulance calls tomorrow → Action: Deploy 12 extra ambulances
            </p>
          </div>
          <DemandForecasting />
        </TabsContent>

        {/* Tab 2: Crisis Prediction */}
        <TabsContent value="crisis" className="space-y-4">
          <div className="bg-orange-50 dark:bg-orange-950 border-l-4 border-orange-500 p-4 rounded-lg">
            <h3 className="font-semibold text-orange-900 dark:text-orange-100 mb-2">
              💡 Use Case: "Will Nagpur face water shortage in next 5 days?"
            </h3>
            <p className="text-sm text-orange-800 dark:text-orange-200">
              <strong>Example:</strong> Input Nagpur + April + 80 water requests + 45% resolved
              → Output: 78% chance of crisis in 5 days → Action: Deploy emergency water tankers now
            </p>
          </div>
          <CrisisPrediction />
        </TabsContent>

        {/* Tab 3: Priority Scoring */}
        <TabsContent value="priority" className="space-y-4">
          <div className="bg-purple-50 dark:bg-purple-950 border-l-4 border-purple-500 p-4 rounded-lg">
            <h3 className="font-semibold text-purple-900 dark:text-purple-100 mb-2">
              💡 Use Case: "We have 10 issues - which one to solve FIRST?"
            </h3>
            <p className="text-sm text-purple-800 dark:text-purple-200">
              <strong>Example:</strong> Test all issues → ICU beds score: 9.8 (CRITICAL), Road pothole: 4.2 (MEDIUM), Water shortage: 8.5 (HIGH)
              → Action: Fix ICU first, then water, then roads
            </p>
          </div>
          <PriorityScoring />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Predictions;
