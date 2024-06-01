/**
 * @id java-kotlin/contain-field
 * @name Contain
 * @description Contain Field
 * @kind problem
 * @problem.severity recommendation
 */

import java

from Field f
where f.getType() instanceof RefType
select f, f.getDeclaringType().getQualifiedName() + " " + ((RefType) f.getType()).getQualifiedName()