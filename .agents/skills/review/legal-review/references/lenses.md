# Review Lenses

Six parallel read-only briefs. Each verifies statutes online where reachable and returns findings ranked by severity with a short "checked and adequate" list. Seed items are leads to verify, refute, or expand, never conclusions.

## Common Instructions For Every Lens

- Aim for the twelve to twenty findings that matter, not an exhaustive list.
- Propose concrete replacement language for every finding.

## Lens A: Contract Formation And Enforceability

Assent and formation (clickwrap versus browsewrap; who is a party; whether every party class
actually holds the identity the mechanics key on), the arbitration clause in full, contractual
limitation periods, limitation of liability, indemnification, licence grants, confidentiality,
term and termination, unilateral modification, notices and electronic signatures, governing law
and venue, definitions and boilerplate. Analyse under the chosen governing law and the Federal
Arbitration Act, noting where other states' consumer law still reaches individuals.

Seed checklist:

- A contractual shortening of the limitations period is void under Fla. Stat. § 95.03 when
  Florida law governs, inside arbitration as well as court.
- A commercial arbitration rule set named for individuals: the administrator applies its consumer
  or workplace rules regardless, requires clause registration, and will decline if unregistered;
  check fee allocation, fallback administrator, seat for individuals, mass-arbitration batching,
  and whether "formation" is delegated (it cannot be).
- Browsewrap phrases ("by continuing", "by accessing") do not bind; the proponent proves assent
  with the actual interface; acceptance records need surface, version, hash, time, address.
- "You" defined as the individual and the organisation makes the clicking employee an indemnitor.
- A product name defined as the service and then used as the contracting party.
- A cap computed on fees "paid us" when a merchant of record collects the fees; missing
  carve-outs for confidentiality, security, indemnity, gross negligence; "lost data" excluded by
  a data custodian.
- A confidentiality clause that forbids the vendor disclosures the service requires.
- A change clause with deemed acceptance, notice only for "material" changes, notice "posted in
  the service", or a carve-out the data model cannot represent.
- Electronic-signature adoption and tax-form jurat language; consumer-consent elements where
  individuals receive statements electronically.
- Survival list gaps; no non-reliance clause where results are disclaimed; no-third-party
  beneficiary clause contradicting indemnitees or transfer clauses.

## Lens B: Regulated Activity

Money transmission and flow of funds, incorporated payments and billing terms, subscription
billing and auto-renewal, tax forms and information reporting, IRS electronic-collection rules,
TIN matching, verification authorizations, AI and agent access, export controls and sanctions.

Seed checklist:

- Read the payout code to find the charge model. A destination charge on the platform account
  without `on_behalf_of` settles to the platform balance before transfer, so "we do not take
  possession of funds" is inaccurate; draft the processor-exemption elements instead (payment for
  services, agreement with the payee, regulated clearance systems) and flag state licensing where
  no processor exemption exists.
- Connected-account agreement acceptance attested by the platform must present the agreement to
  the account holder and record that person's address and date; a payments capability requested on
  the connected account forces the full agreement.
- An ACH debit needs a mandate the payer saw; an "offline" mandate flag without mandate text is a
  gap.
- Fetch the billing provider's buyer and merchant terms. A merchant of record sets refunds, taxes,
  and payment authority; the document must say who the seller of record is and which document
  controls a conflict.
- Electronic W-9 and W-8 systems must present the official certification, obtain the payee's own
  signature under penalties of perjury, log access, and produce a hard copy; a Business must not
  be able to sign a payee's form.
- IRS TIN Matching is available only to payers and their authorized agents; the document needs the
  designation and use restriction.
- Auto-renewal statutes largely exempt business purchasers, but the merchant-of-record contract
  usually requires ROSCA-style disclosures and online cancellation; check the current status of
  the FTC negative-option rule rather than assuming it.
- Sanctions: never describe screening the product does not do; allocate payee screening to the
  Business and reserve a right to block.
- State that the platform does not withhold, prepare, or file information returns, and whether it
  is a third-party settlement organisation.
- AI features: name the provider class, state no-training and retention terms, and distinguish
  features the platform operates from agents the user connects.
- Sector overlays: fintech (GLBA, state money-transmission licensing, Reg E for consumer
  accounts); employment-adjacent (FCRA for any consumer-report-derived signal, worker
  classification indemnities, backup withholding responsibility).

## Lens C: US Privacy And Consumer Protection

CCPA and CPRA including the notice at collection, retention by category, request methods,
sensitive-information limits, and automated-decision rules; other comprehensive state laws and
their commercial-context exemptions; FCRA and GLBA basis for identity checks; TCPA and state
telemarketing law for SMS; CAN-SPAM; state breach-notification duties including the third-party
agent clock; state SSN-privacy statutes; FTC Act § 5 and state UDAP exposure for voluntary
statements.

Seed checklist:

- Is the policy published and linked where the documents say it is? A notice nobody can reach
  gives notice to nobody.
- Is a notice at collection shown where SSN, date of birth, address, and phone are entered?
- Do the source cells of the categories table name the verification providers as a source?
- Does the verification section claim a GLBA "consent" the terms never contain? Credit-header
  data flows under GLBA exceptions, not consent; state the exception relied on.
- Does the code map every check to an FCRA "legitimate business need" while the accepted terms
  are the consumer's written instruction? Does any check run before acceptance?
- If a report-derived status shapes whether a Business works with or pays someone, assess the
  employment-purpose stack for independent contractors and tag it `[review]`.
- Breach: does either document commit to notify Businesses within the third-party-agent window and
  individuals within the statutory window?
- Retention: are stated periods enforced by anything? Is retention stated per category?
- Does the policy describe analytics, cookies, or screening that do not exist? A voluntary
  statement is an enforceable representation regardless of statutory thresholds.
- Automated decisions: does any gate deny compensation without a human path, and is that
  described?
- Request methods and contact details present where the rights are listed.
- SMS consent at the point the number is collected; STOP and HELP keywords in the binding
  document.

## Lens D: Controller-Processor Structure And International

Processor contract content under CCPA regulations and the state processor laws, GDPR Article 28
terms, applicability of non-US law to a product that onboards foreign contractors, transfer
mechanisms, subprocessors, request routing, breach assistance, deletion and return, training on
customer data, de-identified data.

Seed checklist:

- Do processor terms apply by default, or only through an addendum "on request"? Without a
  compliant contract the platform is not a service provider at all for California data.
- Walk the addendum terms as a table: roles, processing scope and instructions, subprocessors and
  change notice, security annex, breach trigger and timeline, audit rights, transfers, deletion
  and return with certification, liability. Mark each present, partial, or absent.
- Foreign payees are expected (a non-US tax form exists), so choose and state a position: restrict
  to US Businesses and residents, or apply the addendum and transfer clauses by default with a
  representative and lawful bases mapped to purposes. "You understand your data is processed in
  the United States" is not a transfer mechanism.
- Controller status claimed over checks the Business requested is a converging-decisions fact
  pattern; fraud and security screening is already permitted to a service provider.
- Retention carve-outs a processor cannot assert (the controller's own tax duty, vendor contracts
  called "law", "legal claims" without a hold, unbounded backups).
- Subprocessors listed by category only, with no change notice or objection right; model
  providers missing from the list; "improve the Services" licence broad enough to cover training.
- De-identified data without the public no-re-identification commitment and flow-down.
- Request routing must either act on instructions or say the request cannot be acted on because it
  reached a service provider, and give both response periods.
- Other regimes a foreign-contractor product reaches: Canada and Quebec, Brazil, Australia (a
  foreign tax number on the non-US form may be a national identifier with its own rules).

## Lens E: Code-Versus-Document Consistency

Verify every factual claim in both documents against the repositories and report each as
consistent, mismatch, or unverifiable, with severity: Critical when the document states something
false; High when it promises a mechanism that does not exist; Medium when partly true.

Claims to check:

- The publication URL of each document resolves in the frontend and is linked from the app.
- Each assent surface the documents name exists and shows the documents; what an acceptance
  record stores.
- Whether the two documents can be versioned independently and what a version change does to
  users' acceptance state.
- The payout charge model, who holds the connected account, and whose address is attested for the
  payments provider's agreement; whether any mandate text exists.
- Whether raw bank details are stored, and how the documents describe payout credentials.
- Whether any information return is generated or filed.
- Which verification steps a user-reachable flow triggers, what those steps return, what is
  surfaced, and whether any step runs before the terms are accepted.
- Whether business verification is a registry check or a reviewed questionnaire.
- Which third parties actually receive data (authentication, email, SMS, hosting, storage, key
  management, model providers) versus the categories the documents list.
- Which cookies and storage the frontend sets; whether any analytics or tracking exists.
- Whether any retention, deletion, closure, export, or grant-revocation mechanism exists behind
  each stated period or promise.
- Whether anything performs sanctions screening.
- Which contact addresses the app itself uses.
- Whether the served legal page renders the document's tables and headings.

## Lens F: Cross-Document Consistency And Drafting

Contradictions between the two documents; every numbered cross-reference resolved against its
target; defined terms used but undefined, defined but unused, or used against their definition;
Markdown and rendering defects; regional spelling and typographic consistency; duplicated
obligations that have drifted; audience mismatch (clauses drafted for one party class binding
another); missing structure (contents, summary, version pointer, consistent contact blocks).

Deliver a defined-terms audit table and a cross-reference audit table in addition to findings.
