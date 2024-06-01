/**
 * @id java-kotlin/return
 * @name Return
 * @description Return
 * @kind problem
 * @problem.severity recommendation
 */

import java

from Callable c, RefType t
where c.getReturnType() = t
select c, c.getQualifiedName() + " " + t.getQualifiedName()