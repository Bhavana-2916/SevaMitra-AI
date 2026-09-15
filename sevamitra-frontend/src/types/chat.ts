export type Language = "English" | "Hindi" | "Telugu";

export type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  service?: ServiceData;
};

export type ServiceData = {
  serviceName: string;
  quickAnswer: string;
  eligibility: string[];
  documents: string[];
  steps: string[];
  fees?: string;
  processingTime?: string;
  officialUrl?: string;
  source?: string;
};
