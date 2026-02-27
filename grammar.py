"""
grammar.py
==========

Implements a simple grammar for Toki Pona.  This module defines
rules that can be used to verify and generate basic Toki Pona
sentences.  It is not a full parser; instead it provides helper
methods for the Ego layer to ensure outputs conform to the
subject–verb–object structure and proper use of particles
such as ``li``, ``e`` and ``o``.
"""

from __future__ import annotations

from typing import List, Tuple, Optional


class TokiPonaGrammar:
    """Minimal grammar and lexicon for Toki Pona."""

    # A small lexicon of words grouped by category.  This can be
    # expanded to include all official root words.
    subjects = {"mi", "sina", "jan"}
    verbs = {"tawa", "moku", "lon", "lukin", "sona"}
    objects = {"kili", "ma", "tomo", "supa"}
    particles = {"li", "e", "o", "la", "pi"}

    def validate(self, tokens: List[str]) -> bool:
        """Validate a token sequence against basic Toki Pona grammar.

        This method implements a simplified grammar:
        - Subject may be "mi" or "sina" without ``li``; otherwise a third
          person subject must be followed by ``li``.
        - Verb must follow subject or ``li``.
        - An object, if present, must be preceded by ``e``.
        Commands starting with ``o`` are also accepted.
        """
        if not tokens:
            return False
        # imperative form: o VERB e OBJ
        if tokens[0] == "o":
            # e.g. o moku e kili
            if len(tokens) < 2 or tokens[1] not in self.verbs:
                return False
            # allow optional object after "e"
            return True
        # declarative: subject [li] verb [e object]
        subject = tokens[0]
        if subject not in self.subjects:
            return False
        idx = 1
        if subject not in {"mi", "sina"}:
            if idx >= len(tokens) or tokens[idx] != "li":
                return False
            idx += 1
        # verb
        if idx >= len(tokens) or tokens[idx] not in self.verbs:
            return False
        idx += 1
        # optional object phrase
        if idx < len(tokens):
            if tokens[idx] != "e":
                return False
            idx += 1
            # at least one object word must follow
            if idx >= len(tokens) or tokens[idx] not in self.objects:
                return False
        return True

    def canonicalise(self, tokens: List[str]) -> List[str]:
        """Return a canonical form of the token sequence.

        This method ensures that the ``li`` and ``e`` particles are
        inserted when required.  It can be used by the Ego to
        correct slightly malformed sentences.
        """
        if not tokens:
            return tokens
        # imperative: insert 'o'
        if tokens[0] == "o":
            return tokens
        subject = tokens[0]
        rest = tokens[1:]
        # automatically insert 'li' if needed
        if subject not in {"mi", "sina"}:
            if not rest or rest[0] != "li":
                rest = ["li"] + rest
        # ensure object phrase uses 'e'
        if len(rest) >= 2 and rest[1] in self.objects and rest[0] in self.verbs:
            rest = [rest[0], "e"] + rest[1:]
        return [subject] + rest

    def default_sentence(self) -> List[str]:
        """Return a simple default sentence for initialisation."""
        return ["mi", "sona"]  # "I know"
