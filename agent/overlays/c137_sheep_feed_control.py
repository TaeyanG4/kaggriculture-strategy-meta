# SPDX-License-Identifier: Apache-2.0
"""Research ablation: retain the parent's sheep feeding; cow logic unchanged.

Disable only c124's late low-margin sheep FEED->PASS substitution. This lets
paired diagnostics measure remaining wool/fertilizer against foregone grain
sales and price feedback. Not a qualified submission candidate.
"""
_C124_PRODUCTS = dict(_C124_PRODUCTS)
_C124_PRODUCTS.pop('SHEEP', None)
