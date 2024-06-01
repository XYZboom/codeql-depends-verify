/**
 * @id java-kotlin/annotation
 * @name Annotation
 * @description Annotation
 * @kind problem
 * @problem.severity recommendation
 */

import java

from Annotation a
where a.getTarget() instanceof RefType
select a, ((RefType) a.getTarget()).getQualifiedName() + " " + a.getType().getQualifiedName()