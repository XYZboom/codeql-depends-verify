/**
 * @id java-kotlin/extend-references
 * @name Extend
 * @description Extend
 * @kind problem
 * @problem.severity recommendation
 */

import java

from RefType child, RefType parent
where child.hasSupertype(parent)
    and parent.getQualifiedName() != "java.lang.Object"
select child, child.getQualifiedName() + " " + child.getAStrictAncestor().getQualifiedName()