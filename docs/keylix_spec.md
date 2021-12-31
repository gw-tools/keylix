# The `keylix` pattern specification

Last updated: *2021-12-30*

This page describes the `keylix-v0.1` pattern specification.




## Introduction

`keylix` is a simple GLOB-like string matching pattern specification intended for searching elements in lists of short strings (keys).

*Note: The name `keylix` is an abbreviation for "key list expressions."*

For example, pattern \``cherries`\` matches "cherries", and pattern \``*cherries*`\` - any string that contains the word cherries. \``apples | oranges`\` matches "apples" or "oranges."

Similarly, \``raspberries & pies`\` matches any string that starts with one of the patterns and contain both "raspberries" and "pies."
Pattern `pineapples & ~(peanuts)` matches strings that contain "pineapples" but do not contain the word "peanuts."




## Expression patterns

A `keylix` expression can constructed with one of the following patterns:

| Pattern | Description | Spec Version |
| ------- | ----------- | ------------ |
| \`\` | Empty pattern | >0.1 |
| A sequence of non-special characters | Any sequence of characters excluding \``~*&\|(){}"`\`, \``\`\` (backslash), \`` `\` (space), and characters with ASCII codes <= 31 (i.e. all special symbols including new line, tab, etc.). | >0.1 |
| \``*`\` | Wildcard | >0.1 |
| \`<code>( <span class="suggest-exp">$SUBX1</span> )</code>\` | An expression enclosed in parentheses. Here, <code><span class="suggest-exp">$SUBX1</span></code> represents a valid `keylix` expression. | >0.1 |
| \`<code>~(<span class="suggest-exp">$SUBX1</span>)</code>\` | EXCLUDES-pattern: a \``~`\` (NOT) operator followed by an expression enclosed in parentheses. | >0.2 |
| \`<code><span class="suggest-exp">$SUBX1</span> & <span class="suggest-exp2">$SUBX2</span> & ...</code>\` | AND-pattern: a sequence of expressions separated by the \``&`\` (AND) operator. | >0.2 |
| \`<code><span class="suggest-exp">$SUBX1</span> \| <span class="suggest-exp2">$SUBX2</span> \| ...</code>\` | OR-pattern: a sequence of espressions separated by the \``\|`\` (OR) operator. | >0.1 |
| \`<code><span class="suggest-exp">$SUBX1</span><span class="suggest-exp2">$SUBX2</span>...</code>\` | CONCAT-pattern: an expression followed by another expression or expressions without a separator in between. | >0.1 |
| Parameters | Work on the parameter support will be considered after the completion of the v0.2 spec implementation. | >=1.0 |
| Match special character | Work on the support for patterns that can match special characters will be considered after the completion of the v0.2 spec implementation. | >=1.0 |

*Note: While the initial spec and the Python module are in the early stages of the development, the "Spec Version" column is used to set implementation priorities in the `keylix` Python module.*

Only sequences with expressions separated by the same operator (either \``|`\` or \``&`\`) are valid. Here are a few examples of valid and invalid patterns:

<ul class="no-bullets">
    <li>`<code>( apples |  | cherries )</code>` <span class="valid">(valid)</span></li>
    <li>`<code>( apples | bananas | cherries )</code>` <span class="valid">(valid)</span></li>
    <li>`<code>( apples <span class="invalid">|</span> bananas <span class="invalid">&</span> ~(zebras) )</code>` <span class="invalid">(invalid)</span></li>
    <li>`<code>( ( apples | bananas ) & ~(zebras) )</code>` <span class="valid">(valid)</span></li>
    <li>`<code>( apples <span class="invalid">|</span> bananas <span class="invalid">&</span> peanuts )</code>` <span class="invalid">(invalid)</span></li>
    <li>`<code>( apple | ( *salad & ~(*peanut*) ) )</code>` <span class="valid">(valid)</span></li>
</ul>

### Empty pattern

The empty pattern matches an empty string.

*Note: Empty pattern expressions in AND-pattern sequences are ignored.*

### Non-special characters

A non special character is is a valid expression.
A sequence of non special characters also forms a valid expression.
A non-special-character expression matchs a string that is equal to the expression.

### Wildcard

Wildcard matches any string including a zero-length string.

### EXCLUDES-pattern

A pattern of the form \`<code>~(<span class="suggest-exp">$SUBX1</span>)</code>\` matches any string that does not match \`<code><span class="suggest-exp">$SUBX1</span></code>\`.

### AND-pattern

The AND-pattern expression matches any string that contains matches to all of the expressions in the AND-pattern sequence, starts with a match to any of the expressions, and ends with a match to one of these expressions.

### OR-pattern

The OR-pattern matches a string that can match any expression in the sequence.

### Space characters

Spaces can be inserted between any token without affecting the match.
They can be used to improve the readability of the pattern.
A single **exception to this rule is the CONCAT-pattern** that does not allow spaces between sub-expressions.
For example, the following expressions are equivalent:

<ul class="no-bullets">
    <li>`<code>((apple(|s)|bananas)&~(zebras))</code>`</li>
    <li>`<code>( (apple(|s)|bananas) & ~(zebras) )</code>`</li>
    <li>`<code>( ( apple(|s) | bananas ) & ~(zebras) )</code>` <-- This is the notation followed in the current document (for the most part).</li>
    <li>`<code>( ( apple(|s) | bananas ) & ~( zebras ) )</code>`</li>
    <li></li>
</ul>

Here are examples of invalid expressions:

<ul class="no-bullets">
    <li>`<code>( ( appl<span class="invalid">e (</span>|s) | bananas ) & ~(zebras) )</code>` <span class="invalid">(invalid)</span><br>
    Expressions `<code>apple</code>` and `<code>(|s)</code>` form a CONCAT-pattern.<br>
    &nbsp;</li>
    <li>`<code>( ( apple(|s) | bananas ) & <span class="invalid">~ (</span>zebras) )</code>` <span class="invalid">(invalid)</span><br>
    Symbols <code>~</code> and <code>(</code> form a single token <code>~(</code>. Outside of special string patterns (planned after v0.2), spaces can be inserted only between tokens.<br>
    &nbsp;</li>
    <li></li>
</ul>




<style type="text/css">
    code{white-space: pre-wrap;}
    span.suggest-exp {color: blue;}
    span.suggest-exp2 {color: purple;}
    ul.no-bullets {list-style-type: none;}
    span.valid {color: green;}
    span.invalid {color: red;}
</style>