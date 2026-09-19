import { useState } from "react";
import { useForm } from "react-hook-form";

import { exportBusinessPlanPdf } from "../api/client";

export default function PdfExportForm() {
  const [error, setError] = useState("");
  const { register, handleSubmit, formState } = useForm({
    defaultValues: {
      executive_summary: "",
      swot: "",
      marketing_plan: "",
      financial_plan: "",
    },
  });

  async function onSubmit(values) {
    setError("");

    try {
      const response = await exportBusinessPlanPdf({
        business_plan: values,
      });
      const url = URL.createObjectURL(response.data);
      const link = document.createElement("a");
      link.href = url;
      link.download = "business-plan.pdf";
      link.click();
      URL.revokeObjectURL(url);
    } catch (requestError) {
      setError(
        requestError.response?.data?.detail ||
          "PDF faylini yaratib bo'lmadi.",
      );
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label>
        Executive Summary
        <textarea {...register("executive_summary", { required: true })} />
      </label>
      <label>
        SWOT
        <textarea {...register("swot", { required: true })} />
      </label>
      <label>
        Marketing Plan
        <textarea {...register("marketing_plan", { required: true })} />
      </label>
      <label>
        Financial Plan
        <textarea {...register("financial_plan", { required: true })} />
      </label>
      <button type="submit" disabled={formState.isSubmitting}>
        {formState.isSubmitting ? "Tayyorlanmoqda..." : "PDF yuklab olish"}
      </button>
      {error && <p role="alert">{error}</p>}
    </form>
  );
}
