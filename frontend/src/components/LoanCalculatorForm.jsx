import { useState } from "react";
import { useForm } from "react-hook-form";

import { calculateLoan } from "../api/client";

export default function LoanCalculatorForm() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const { register, handleSubmit, formState } = useForm({
    defaultValues: {
      principal: "",
      term_months: "",
      annual_interest_rate: "",
      monthly_income: "",
    },
  });

  async function onSubmit(values) {
    setError("");
    setResult(null);

    try {
      const response = await calculateLoan({
        principal: Number(values.principal),
        term_months: Number(values.term_months),
        annual_interest_rate: Number(values.annual_interest_rate),
        monthly_income: Number(values.monthly_income),
      });
      setResult(response.data);
    } catch (requestError) {
      setError(
        requestError.response?.data?.detail ||
          "Kredit hisob-kitobini bajarib bo'lmadi.",
      );
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label>
        Sarmoya
        <input
          type="number"
          min="0.01"
          step="0.01"
          {...register("principal", { required: true, min: 0.01 })}
        />
      </label>
      <label>
        Muddat (oy)
        <input
          type="number"
          min="1"
          step="1"
          {...register("term_months", { required: true, min: 1 })}
        />
      </label>
      <label>
        Yillik foiz
        <input
          type="number"
          min="0"
          step="0.01"
          {...register("annual_interest_rate", { required: true, min: 0 })}
        />
      </label>
      <label>
        Oylik daromad
        <input
          type="number"
          min="0.01"
          step="0.01"
          {...register("monthly_income", { required: true, min: 0.01 })}
        />
      </label>
      <button type="submit" disabled={formState.isSubmitting}>
        {formState.isSubmitting ? "Hisoblanmoqda..." : "Hisoblash"}
      </button>
      {error && <p role="alert">{error}</p>}
      {result && (
        <section aria-live="polite">
          <p>Oylik to&apos;lov: {result.monthly_payment}</p>
          <p>Jami to&apos;lov: {result.total_payment}</p>
          {result.risk_warning && <p role="alert">{result.risk_warning}</p>}
        </section>
      )}
    </form>
  );
}
