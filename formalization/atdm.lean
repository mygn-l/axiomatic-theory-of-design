-- Symbol introduction
axiom ATDM_Object : Type

axiom subset_of : ATDM_Object → ATDM_Object → Prop
infix:50 "⊆" => subset_of

axiom related : ATDM_Object → ATDM_Object → ATDM_Object
infix:75 "⊗" => related

-- Real axioms

axiom extensionality :
  ∀ A B : ATDM_Object,
    (∀ x, x ⊆ A ↔ x ⊆ B) → A = B

axiom empty :
  ∃ B : ATDM_Object,
    ∀ x, ¬ (x ⊆ B)

def is_union (A B C : ATDM_Object) : Prop :=
  ∀ x, x ⊆ C ↔ x ⊆ A ∨ x ⊆ B

axiom union :
  ∀ A B : ATDM_Object,
    ∃ C : ATDM_Object, is_union A B C

theorem union_unique :
  ∀ A B C D : ATDM_Object,
    is_union A B C ∧
    is_union A B D →
      C = D := by
        intro A B C D h
        apply extensionality
        intro x
        constructor
        · intro hC
          exact (h.right x).mpr ((h.left x).mp hC)
        · intro hD
          exact (h.left x).mpr ((h.right x).mp hD)

-- is_union quickly becomes very cumbersome
-- so we define a canonical union object to equal the union
-- although it doesn't depend on the uniqueness theorem
-- we will use this little hack

noncomputable def get_union (A B : ATDM_Object) : ATDM_Object :=
  Classical.choose (union A B)
infix:65 "⊔" => get_union

theorem union_associativity :
  ∀ A B C : ATDM_Object,
    (A ⊔ B) ⊔ C = A ⊔ (B ⊔ C) := by
      intro A B C

      have hAB : ∀ x, x ⊆ A ⊔ B ↔ x ⊆ A ∨ x ⊆ B :=
        Classical.choose_spec (union A B)
      have hABC_left : ∀ x, x ⊆ (A ⊔ B) ⊔ C ↔ x ⊆ A ⊔ B ∨ x ⊆ C :=
        Classical.choose_spec (union (A ⊔ B) C)
      have hBC : ∀ x, x ⊆ B ⊔ C ↔ x ⊆ B ∨ x ⊆ C :=
        Classical.choose_spec (union B C)
      have hABC_right : ∀ x, x ⊆ A ⊔ (B ⊔ C) ↔ x ⊆ A ∨ x ⊆ B ⊔ C :=
        Classical.choose_spec (union A (B ⊔ C))

      apply extensionality
      intro x
      rw [hABC_left x, hABC_right x, hAB x, hBC x]
      constructor
      · intro l
        cases l with
        | inl ab =>
            cases ab with
            | inr b => exact Or.inr (Or.inl b)
            | inl a => exact Or.inl a
        | inr c =>
            exact Or.inr (Or.inr c)
      · intro r
        cases r with
        | inl a =>
            exact Or.inl (Or.inl a)
        | inr bc =>
            cases bc with
            | inr c => exact Or.inr c
            | inl b => exact Or.inl (Or.inr b)

theorem union_commutativity :
  ∀ A B : ATDM_Object,
    A ⊔ B = B ⊔ A := by
      intro A B

      have hAB : ∀ x, x ⊆ A ⊔ B ↔ x ⊆ A ∨ x ⊆ B :=
        Classical.choose_spec (union A B)
      have hBA : ∀ x, x ⊆ B ⊔ A ↔ x ⊆ B ∨ x ⊆ A :=
        Classical.choose_spec (union B A)

      apply extensionality
      intro x
      rw [hAB, hBA]
      constructor
      · intro l
        cases l with
        | inl a => exact Or.inr a
        | inr b => exact Or.inl b
      · intro r
        cases r with
        | inl b => exact Or.inr b
        | inr a => exact Or.inl a

def is_intersection (A B C : ATDM_Object) : Prop :=
  ∀ x, x ⊆ C ↔ x ⊆ A ∧ x ⊆ B

axiom intersection :
  ∀ A B : ATDM_Object,
    ∃ C : ATDM_Object,
      is_intersection A B C

axiom subset :
  ∀ A : ATDM_Object,
    ∃ B : ATDM_Object,
      B ⊆ A

axiom relation :
  ∀ A B : ATDM_Object,
    ∃ C : ATDM_Object,
      C = A ⊗ B

axiom relation_right_distributivity :
  ∀ A B C : ATDM_Object,
    A ⊗ (B ⊔ C) = (A ⊗ B) ⊔ (A ⊗ C)
axiom relation_left_distributivity :
  ∀ A B C : ATDM_Object,
    (A ⊔ B) ⊗ C = (A ⊗ C) ⊔ (B ⊗ C)

noncomputable def struct (A : ATDM_Object) : ATDM_Object :=
  A ⊔ (A ⊗ A)
prefix:80 "⊕" => struct

theorem decomposition :
  ∀ A B C : ATDM_Object,
    (A = B ⊔ C) →
      (⊕A = ((⊕B ⊔ ⊕C) ⊔ (B ⊗ C)) ⊔ (C ⊗ B)) := by
        intro A B C h
        unfold struct
        rw [h]
        rw [relation_left_distributivity]
        rw [relation_right_distributivity]
        sorry
        -- very tedious
        -- simply do a bunch of swaps and parenthesis changes
        -- in order to get the same shape on both sides

axiom nature : ATDM_Object

axiom human_thought_exist_bounded :
  ∃ M : ATDM_Object,
    ∃ k : Nat, ∃ f : Fin k → ATDM_Object,
      ∀ x : ATDM_Object, x ⊆ M → ∃ n, f n = x
-- Note: natural numbers are introduced
noncomputable def human_thought : ATDM_Object :=
  Classical.choose (human_thought_exist_bounded)

noncomputable def world : ATDM_Object :=
  nature ⊔ human_thought

noncomputable def natural_system : ATDM_Object :=
  ⊕nature

noncomputable def natural_law : ATDM_Object :=
  Classical.choose (subset natural_system)

noncomputable def rational_system : ATDM_Object :=
  ⊕human_thought

noncomputable def knowledge : ATDM_Object :=
  Classical.choose (subset rational_system)

noncomputable def recognition : ATDM_Object :=
  Classical.choose (subset (nature ⊗ human_thought))

noncomputable def human_action : ATDM_Object :=
  Classical.choose (subset (human_thought ⊗ nature))

theorem knowledge_limited :
  ∃ k : Nat, ∃ f : Fin k → ATDM_Object,
    ∀ x : ATDM_Object, x ⊆ knowledge → ∃ n, f n = x := by
      sorry

--TODO: Axiom of recognition and Axiom of causality

axiom product_exist :
  ∃ S : ATDM_Object, S ⊆ nature
noncomputable def product : ATDM_Object :=
  Classical.choose (product_exist)

def is_complement (A B C : ATDM_Object) : Prop :=
  ∀ x : ATDM_Object,
    (x ⊆ C) ↔ (x ⊆ A ∧ ¬(x ⊆ B))
axiom complement :
  ∀ A B : ATDM_Object,
    ∃ C : ATDM_Object,
      is_complement A B C
noncomputable def get_complement (A B : ATDM_Object) : ATDM_Object :=
  Classical.choose (complement A B)
infix:60 "-" => get_complement

noncomputable def env : ATDM_Object :=
  nature - product

theorem nature_product_env :
  nature = env ⊔ product := by
    have iE : ∀ x, (x ⊆ env) ↔ (x ⊆ nature ∧ ¬(x ⊆ product)) :=
      Classical.choose_spec (complement nature product)

    apply extensionality
    intro x
    sorry
    /-
    constructor
    · intro l
    · intro r
    -/

theorem engineering_system :
  ⊕nature = (⊕env) ⊔ ((⊕product) ⊔ ((env ⊗ product) ⊔ (product ⊗ env))) := by
    rw [struct, struct, struct]
    rw [nature_product_env]
    rw [relation_left_distributivity]
    rw [relation_right_distributivity, relation_right_distributivity]
    sorry
    -- Again, a bunch of commutativity and associativity swaps like before

--TODO: performance, etc
