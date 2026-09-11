"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";

type Candidate = {
  canonical_name: string;
  supportive_media_spend: number;
  opposition_media_spend: number;
  total_media_activity: number;
  votes: number;
  vote_share: number;
};

type FeaturedInsight = {
  candidate: string;
  supportive_media_share: number;
  opposition_media_share: number;
  vote_share: number;
};

type Investigation = {
  question: string;
  finding: string;
  evidence: string[];
  interpretation: string;
  counter_evidence: string[];
  limitations: string[];
  confidence: string;
};

type Summary = {
  total_media_activity: number;
  total_votes: number;
  candidates: Candidate[];
  featured_insight: FeaturedInsight;
};

const money = (value: number) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(value);

const number = (value: number) =>
  new Intl.NumberFormat("en-US").format(value);

export default function Home() {
  const [investigation, setInvestigation] = useState<Investigation | null>(null);
  const [data, setData] = useState<Summary | null>(null);

  useEffect(() => {
    Promise.all([
      fetch("/data/summary.json").then((response) => response.json()),
      fetch("/data/investigation.json").then((response) => response.json()),
    ]).then(([summary, investigation]) => {
      setData(summary);
      setInvestigation(investigation);
    });
  }, []);

  if (!data) {
    return <main className={styles.main}>Loading...</main>;
  }

  return (
    <main className={styles.main}>
      <header>
        <p className={styles.eyebrow}>
          Advertising Decision Intelligence
        </p>

        <h1>2025 NYC Mayoral Media Intelligence</h1>

        <p className={styles.subtitle}>
          Paid-media activity, independent spending, and election outcomes
          derived from public NYC election data.
        </p>
      </header>

      <section className={styles.metrics}>
        <div className={styles.card}>
          <span>Total media activity</span>
          <strong>{money(data.total_media_activity)}</strong>
        </div>

        <div className={styles.card}>
          <span>Total candidate votes</span>
          <strong>{number(data.total_votes)}</strong>
        </div>
      </section>

      <section className={styles.insight}>
        <p className={styles.eyebrow}>Key signal</p>

        <h2>
          Mamdani captured{" "}
          {(data.featured_insight.vote_share * 100).toFixed(1)}% of the vote
          with only{" "}
          {(data.featured_insight.supportive_media_share * 100).toFixed(0)}%
          of supportive media spend.
        </h2>

        <p>
          He was also the target of{" "}
          {(data.featured_insight.opposition_media_share * 100).toFixed(0)}%
          of opposition media activity. This shows a substantial divergence
          between paid-media investment and electoral performance, but does
          not establish causation.
        </p>
      </section>

      <section className={styles.analysis}>
        <div>
        <p className={styles.eyebrow}>Attention signal</p>
        <h2>Paid media and public attention did not always move together</h2>
        <p>
         Mamdani&apos;s Wikipedia attention share materially exceeded his share
          of paid-media activity around several periods, including the June
          primary. Wikipedia pageviews are treated as an attention signal, not
          voter sentiment or evidence of advertising effectiveness.
        </p>
        </div>

        <img
          className={styles.chart}
          src="/images/mamdani-media-attention.png"
          alt="Mamdani paid media activity share compared with Wikipedia attention share"
        />
      </section>

      {investigation && (
      <section className={styles.investigation}>
      <p className={styles.eyebrow}>AI evidence synthesis</p>
      <div className={styles.aiProvenance}>
        <span>Local LLM</span>
        <span>Structured evidence only</span>
        <span>Grounding validated</span>
        <span>Static published output</span>
      </div>

      <h2>{investigation.question}</h2>

      <div className={styles.finding}>
        <strong>Finding</strong>
        <p>{investigation.finding}</p>
      </div>

      <div className={styles.investigationGrid}>
        <div>
          <h3>Supporting evidence</h3>
          <ul>
            {investigation.evidence.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>

        <div>
          <h3>Counter-evidence</h3>
          <ul>
            {investigation.counter_evidence.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </div>

      <p className={styles.interpretation}>
        {investigation.interpretation}
      </p>

      <p className={styles.confidence}>
        Evidence confidence: <strong>{investigation.confidence}</strong>
      </p>
    </section>
    )}

      <section>
        <h2>Candidate media environment</h2>

        <div className={styles.tableWrapper}>
          <table>
            <thead>
              <tr>
                <th>Candidate</th>
                <th>Supportive media</th>
                <th>Opposition media</th>
                <th>Total activity</th>
                <th>Vote share</th>
              </tr>
            </thead>

            <tbody>
              {data.candidates.map((candidate) => (
                <tr key={candidate.canonical_name}>
                  <td>{candidate.canonical_name}</td>
                  <td>{money(candidate.supportive_media_spend)}</td>
                  <td>{money(candidate.opposition_media_spend)}</td>
                  <td>{money(candidate.total_media_activity)}</td>
                  <td>{(candidate.vote_share * 100).toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}