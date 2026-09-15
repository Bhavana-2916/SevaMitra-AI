import {
  CheckCircle2,
  FileText,
  ListChecks,
  ExternalLink,
  IndianRupee,
  Clock,
} from "lucide-react";

import { ServiceData } from "@/types/chat";

interface ServiceCardProps {
  service: ServiceData;
}

export default function ServiceCard({ service }: ServiceCardProps) {
  return (
    <div className="mt-4 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm dark:border-slate-700 dark:bg-slate-900">
      {/* Header */}
      <div className="border-b bg-slate-50 p-5 dark:border-slate-700 dark:bg-slate-800">
        <h3 className="text-lg font-bold text-slate-900 dark:text-white">
          {service.serviceName}
        </h3>

        <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">
          {service.quickAnswer}
        </p>
      </div>

      <div className="space-y-6 p-5">
        {/* Eligibility */}
        <section>
          <div className="mb-3 flex items-center gap-2 font-semibold">
            <CheckCircle2 size={19} className="text-green-600" />
            Eligibility
          </div>

          <ul className="space-y-2">
            {service.eligibility.map((item, index) => (
              <li key={index} className="text-sm text-slate-600 dark:text-slate-300">
                • {item}
              </li>
            ))}
          </ul>
        </section>

        {/* Documents */}
        <section>
          <div className="mb-3 flex items-center gap-2 font-semibold">
            <FileText size={19} />
            Required Documents
          </div>

          <ul className="space-y-2">
            {service.documents.map((item, index) => (
              <li key={index} className="text-sm text-slate-600 dark:text-slate-300">
                • {item}
              </li>
            ))}
          </ul>
        </section>

        {/* Steps */}
        <section>
          <div className="mb-3 flex items-center gap-2 font-semibold">
            <ListChecks size={19} />
            Application Steps
          </div>

          <ol className="space-y-3">
            {service.steps.map((step, index) => (
              <li
                key={index}
                className="flex gap-3 text-sm text-slate-600 dark:text-slate-300"
              >
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-blue-100 text-xs font-bold text-blue-700 dark:bg-blue-950 dark:text-blue-300">
                  {index + 1}
                </span>
                {step}
              </li>
            ))}
          </ol>
        </section>

        {/* Fees / processing */}
        {(service.fees || service.processingTime) && (
          <div className="grid gap-3 sm:grid-cols-2">
            {service.fees && (
              <div className="rounded-xl bg-slate-50 p-4 dark:bg-slate-800">
                <div className="flex items-center gap-2 text-sm font-semibold">
                  <IndianRupee size={17} />
                  Fees
                </div>
                <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">
                  {service.fees}
                </p>
              </div>
            )}

            {service.processingTime && (
              <div className="rounded-xl bg-slate-50 p-4 dark:bg-slate-800">
                <div className="flex items-center gap-2 text-sm font-semibold">
                  <Clock size={17} />
                  Processing
                </div>
                <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">
                  {service.processingTime}
                </p>
              </div>
            )}
          </div>
        )}

        {/* Official link */}
        {service.officialUrl && (
          <a
            href={service.officialUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center gap-2 rounded-xl bg-blue-700 px-5 py-3 text-sm font-semibold text-white hover:bg-blue-800"
          >
            Apply on Official Website
            <ExternalLink size={17} />
          </a>
        )}

        {/* Source */}
        {service.source && (
          <p className="text-xs text-slate-500">Source: {service.source}</p>
        )}
      </div>
    </div>
  );
}
